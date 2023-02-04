from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import models
from . import forms


def projects(request):
    all_projects = models.Project.objects.all().order_by('-created')

    context = {
        'projects': all_projects,
    }
    return render(request, 'app_main/projects.html', context)


@login_required(login_url='login')
def project_create(request):
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            messages.success(request, 'Project successfully created')
            return redirect('project_detail', pk=project.id)
        else:
            messages.error(request, 'Fields filled incorrectly')
            return redirect('create_project')

    form = forms.ProjectForm()
    context = {
        'form': form,
        'btn_text': 'Create project'
    }
    return render(request, 'form_template.html', context)


def project_detail(request, pk):
    project = models.Project.objects.get(id=pk)

    if request.method == 'POST':
        profile = request.user.profile
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = profile
            review.project = project
            review.save()
            messages.success(request, 'Successfully commented')
            return redirect('project_detail', pk=pk)

    context = {
        'project': project,
    }
    return render(request, 'app_main/project.html', context)


@login_required(login_url='login')
def project_update(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = forms.ProjectForm(instance=project)

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project successfully updated')
            return redirect('project_detail', pk=project.id)
        else:
            messages.error(request, 'Form filled incorrectly')
            return redirect('project_update', pk=project.id)

    context = {
        'form': form,
        'btn_text': 'Update project',
        'project': project,
    }
    return render(request, 'app_main/project_update.html', context)


@login_required(login_url='login')
def project_delete(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project successfully deleted')
        return redirect('account')

    context = {
        'obj_name': project.name,
        'obj_type': 'project',
    }
    return render(request, 'delete_form.html', context)
