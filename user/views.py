from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import must_not_login
from django.db.models import Count, Q
from django.contrib import messages
from .models import Profile, Skill, Message
from django.core.mail import EmailMessage
from django.conf import settings
import os

def index(request):    
    # Query Data
    search_query = request.GET.get('search_query', '')
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(first_name__icontains=search_query) | 
        Q(last_name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skills__in=skills)
    )

    # Pagination
    items_per_page = 9
    page = request.GET.get('page')
    range_culculation_page = page
    paginator = Paginator(profiles, items_per_page)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
        range_culculation_page = 1
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    # Fix Alot of pages problem
    leftIndex = (int(range_culculation_page) - 4) if not (int(range_culculation_page) - 4) < 1 else 1
    rightIndex = (int(range_culculation_page) + 5) if not (int(range_culculation_page) + 5) > paginator.num_pages else paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)    
        
    return render(request, 'profile/index.html', {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range})

def show(request, id):
    profile = Profile.objects.get(id=id)
    top_skills = profile.skills.exclude(description='')
    other_skills = profile.skills.filter(description='')

    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills
    }
    return render(request, 'profile/show.html', context)

@must_not_login(fallback_url='profile_index')
def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'].lower(), password=request.POST['password'])
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
            try:
                mail = EmailMessage(
                    subject='Welcome to DevCommunity', 
                    body='We are glad you are here! Please find the attachment as our terms and conditions', 
                    from_email=settings.EMAIL_HOST_USER, 
                    to=[user.email]
                    )
                mail.attach_file(os.path.join(settings.MEDIA_ROOT, 'default_profile.png'))
                mail.send()
            except:
                pass
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
@login_required(login_url='profile_login')
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

@login_required(login_url='profile_login')
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

@login_required(login_url='profile_login')
def account_skills_delete(request, id):
    skill = Skill.objects.get(id=id)
    skill.delete()
    messages.success(request, f'Skill Added { skill.name }')
    return redirect('profile_account')


@login_required(login_url='profile_login')
def account_inbox(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'profile/account_inbox.html', context)

@login_required(login_url='profile_login')
def account_inbox_single(request, id):
    message = Message.objects.get(id=id)
    context = {'message': message}

    if not message.is_read:
        message.is_read = True
        message.save()

    return render(request, 'profile/account_inbox_single.html', context)

def account_inbox_create(request, receiver_id):
    receiver = Profile.objects.get(id=receiver_id)
    form = MessageForm()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.receiver = receiver
            if request.user.is_authenticated:
                message.sender = request.user.profile
                message.email = request.user.email
                message.name = request.user.profile.full_name
            message.save()
            messages.success(request, 'Your message has been sent.')
            return redirect('profile_show', receiver.id)

    context = { 'form': form, 'receiver': receiver }
    return render(request, 'profile/account_inbox_create.html', context)

