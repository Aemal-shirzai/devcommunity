from django import forms
from django.forms import ModelForm
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        exclude = ('owner',)
        widgets = { 
            'tags': forms.CheckboxSelectMultiple()
        }
        labels = {
            'tags': 'Already existed tags.'
        }
        
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input', 'placeholder': name.replace('_', ' ').capitalize()})


class ReviewForm(ModelForm):
    
    class Meta:
        model = Review
        fields = ("value", 'body')
        labels = {
            'value': 'Place Your Vote Here.',
            'body': 'Comment Here',
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})