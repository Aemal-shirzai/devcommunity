from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from .forms import CustomUserCreationForm

def must_not_login(fallback_url):
    def decorator(function):
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.user.is_authenticated:
                return redirect(fallback_url)
            return function(*args, **kwargs)
        return wrapper
    return decorator

def index(request):
    profiles = Profile.objects.all()
    return render(request, 'profile/index.html', {'profiles': profiles})

def show(request, id):
    profile = Profile.objects.get(id=id)
    projects = profile.projects \
        .annotate(up_reviews_count=Count('reviews', filter=Q(reviews__value='up'))) \
        .annotate(down_reviews_count=Count('reviews', filter=Q(reviews__value='down')))
    top_skills = profile.skills.exclude(description='')
    other_skills = profile.skills.filter(description='')
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
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            messages.success(request, 'Account created seccessfully. Login Now')
            return redirect('profile_login')

    context = {'form': form}
    return render(request, 'profile/register.html', context)