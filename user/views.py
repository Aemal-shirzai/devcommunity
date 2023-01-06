from django.shortcuts import render
from .models import Profile
from django.db.models import Count, Q

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