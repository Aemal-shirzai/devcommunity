from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Skill

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(forms.ModelForm):
    
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        labels = {
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = user.username.lower()
        if commit:
            user.save()
        return user