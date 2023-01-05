from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.db.models import Count, Q

# Create your views here.
def index(request):
    projects = Project.objects.all() \
        .annotate(up_reviews_count=Count('reviews', filter=Q(reviews__value='up'))) \
        .annotate(down_reviews_count=Count('reviews', filter=Q(reviews__value='down')))
    return render(request, 'project/index.html', {'projects': projects})

def show(request, id):
    project = Project.objects.get(id=id)
    return render(request, 'project/show.html', {'project': project})

def create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_index')

    context = { 'form': form }
    return render(request, 'project/create_edit.html', context)

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

@require_POST
def delete(request, id):
    project = Project.objects.get(id=id)
    if project.featured_image:
        project.featured_image.delete()
    project.delete()
    return redirect('project_index')
