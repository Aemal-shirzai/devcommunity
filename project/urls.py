from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="project_index"),
    path('project/create', views.create, name="project_create"),
    path('project/edit/<int:id>', views.edit, name="project_edit"),
    path('project/delete/<int:id>', views.delete, name="project_delete"),
    path('project/<int:id>', views.show, name="project_show")
]
