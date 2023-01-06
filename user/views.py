from django.shortcuts import render
from .models import Profile

def index(request):
    profiles = Profile.objects.all()
    return render(request, 'profile/index.html', {'profiles': profiles})