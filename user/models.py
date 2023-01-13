from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    short_intro = models.CharField(max_length=250)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=250, null=True)
    profile_image = models.ImageField(upload_to='profiles', default='default_profile.png')
    social_github = models.CharField(max_length=500, null=True, blank=True)
    social_twitter = models.CharField(max_length=500, null=True, blank=True)
    social_linkedin = models.CharField(max_length=500, null=True, blank=True)
    social_stackoverflow = models.CharField(max_length=500, null=True, blank=True)
    social_youtube = models.CharField(max_length=500, null=True, blank=True)
    social_website = models.CharField(max_length=500, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    @property
    def is_active_profile(self):
        return True if self.user and self.user.is_active else False
    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    profile = models.ForeignKey(Profile, related_name='skills', on_delete=models.CASCADE)

    def __str__(self):
        return self.name