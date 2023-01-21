from django.urls import path, include
from . import views

urlpatterns = [
  path('projects', views.get_projects, name='api_get_projects'),
  path('projects/<int:id>', views.get_project, name='api_get_project')
]