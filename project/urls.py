from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="project_index"),
    path('create', views.create, name="project_create"),
    path('edit/<int:id>', views.edit, name="project_edit"),
    path('delete/<int:id>', views.delete, name="project_delete"),
    path('<int:id>', views.show, name="project_show")
]
