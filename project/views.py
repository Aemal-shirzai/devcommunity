from django.views.decorators.http import require_http_methods, require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.http import HttpResponse
from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
from django.contrib import messages

def index(request):

    # Query
    search_query = request.GET.get('search_query', '')
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.all().distinct().filter(
        Q(title__icontains=search_query) | 
        Q(owner__first_name__icontains=search_query) |
        Q(owner__last_name__icontains=search_query) |
        Q(tags__in=tags)
    )

    # Pagination
    items_per_page = 9
    page = request.GET.get('page')
    range_culculation_page = page
    paginator = Paginator(projects, items_per_page)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
        range_culculation_page = 1
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    # Fix Alot of pages problem
    leftIndex = (int(range_culculation_page) - 4) if not (int(range_culculation_page) - 4) < 1 else 1
    rightIndex = (int(range_culculation_page) + 5) if not (int(range_culculation_page) + 5) > paginator.num_pages else paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)
        
    return render(request, 'project/index.html', {'projects': projects, 'search_query': search_query, 'custom_range': custom_range})

def show(request, id):
    project = Project.objects.get(id=id)

    reviews_form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if not request.user.is_authenticated:
            messages.warning(request, 'You Need to login First')
            return redirect('project_show', project.id)
        
        if project.is_owner(request=request):
            messages.warning(request, 'You can not vote for your project')
            return redirect('project_show', project.id)

        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            messages.success(request, 'Thank You! your reviews has been added.')
            return redirect('project_show', project.id)

    return render(request, 'project/show.html', {'project': project, 'form': reviews_form})

@login_required(login_url='profile_login')
def create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user and request.user.profile or False
            project.save()
            # Add tags from already existed tags
            project.tags.set(form.cleaned_data['tags'])
            # Add New tags
            if request.POST.get('new_tags', False):
                new_tags = request.POST['new_tags'].split(',')
                for new_tag in new_tags:
                    tag, created = Tag.objects.get_or_create(name=new_tag.strip())
                    project.tags.add(tag)
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
            project = form.save(commit=False)
            project.owner = request.user and request.user.profile or False
            project.save()

             # Add tags from already existed tags
            project.tags.set(form.cleaned_data['tags'])

            # Add New tags
            if request.POST.get('new_tags', False):
                new_tags = request.POST['new_tags'].split(',')
                for new_tag in new_tags:
                    tag, created = Tag.objects.get_or_create(name=new_tag.strip())
                    project.tags.add(tag)

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

