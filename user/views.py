from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .decorators import must_not_login
from django.db.models import Count, Q
from django.contrib import messages
from .models import Profile, Skill

def index(request):
    profiles = Profile.objects.all()
    return render(request, 'profile/index.html', {'profiles': profiles})

def show(request, id):
    profile = Profile.objects.get(id=id)
    top_skills = profile.skills.exclude(description='')
    other_skills = profile.skills.filter(description='')
    projects = profile.projects \
        .annotate(up_reviews_count=Count('reviews', filter=Q(reviews__value='up'))) \
        .annotate(down_reviews_count=Count('reviews', filter=Q(reviews__value='down')))

    context = {
        'profile': profile,
        'projects': projects,
        'top_skills': top_skills,
        'other_skills': other_skills
    }
    return render(request, 'profile/show.html', context)

@must_not_login(fallback_url='profile_index')
def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            url = 'profile_index' if not request.GET.get('next') else request.GET.get('next')
            return redirect(url)
        else:
            messages.error(request, 'Invalid Username or Password')
    return render(request, 'profile/login.html')

@login_required(login_url='profile_login')
def logout_user(request):
    logout(request)
    return redirect('profile_login')

@must_not_login(fallback_url='profile_index')
def register_user(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created seccessfully. Login Now')
            return redirect('profile_login')

    context = {'form': form}
    return render(request, 'profile/register.html', context)


@login_required(login_url='profile_login')
def account(request):
    profile = request.user.profile
    projects = profile.projects \
        .annotate(up_reviews_count=Count('reviews', filter=Q(reviews__value='up'))) \
        .annotate(down_reviews_count=Count('reviews', filter=Q(reviews__value='down')))
    return render(request, 'profile/account.html', {'profile': profile, 'projects': projects})

@login_required(login_url='profile_login')
def account_edit(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Updated')
            return redirect('profile_account')

    context = { 'form': form }
    return render(request, 'profile/account_edit.html', context)


# Skills
def account_skills_create(request):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = request.user.profile
            skill.save()
            messages.success(request, f'New Skill Added { request.POST["name"] }')
            return redirect('profile_account')

    context = { 'form': form }
    return render(request, 'profile/account_skills_create_edit.html', context)

def account_skills_edit(request, id):
    skill = Skill.objects.get(id=id)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f'Skill Added { request.POST["name"] }')
            return redirect('profile_account')

    context = { 'form': form }
    return render(request, 'profile/account_skills_create_edit.html', context)


def account_skills_delete(request, id):
    skill = Skill.objects.get(id=id)
    skill.delete()
    messages.success(request, f'Skill Added { skill.name }')
    return redirect('profile_account')