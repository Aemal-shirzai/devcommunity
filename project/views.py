from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.http import HttpResponse
from .forms import ProjectForm
from .models import Project

def index(request):
    projects = Project.objects.all() \
        .annotate(up_reviews_count=Count('reviews', filter=Q(reviews__value='up'))) \
        .annotate(down_reviews_count=Count('reviews', filter=Q(reviews__value='down')))
    return render(request, 'project/index.html', {'projects': projects})

def show(request, id):
    project = Project.objects \
        .annotate(up_reviews_count=Count('reviews', filter=Q(reviews__value='up'))) \
        .annotate(down_reviews_count=Count('reviews', filter=Q(reviews__value='down'))) \
        .get(id=id)
    return render(request, 'project/show.html', {'project': project})

@login_required(login_url='profile_login')
def create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_index')

    context = { 'form': form }
    return render(request, 'project/create_edit.html', context)

@login_required(login_url='profile_login')
def edit(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_show', project.id)

    context = { 'form': form }
    return render(request, 'project/create_edit.html', context)

@login_required(login_url='profile_login')
@require_POST
def delete(request, id):
    project = Project.objects.get(id=id)
    if project.featured_image and project.featured_image.name != 'default.png':
        project.featured_image.delete()
    project.delete()
    return redirect('project_index')
