from django.contrib import messages
from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404, redirect, render

from boostlab_tasks.forms import ActivityCreateForm, FileCreateForm, TaskCreateForm, TaskEditForm
from .models import Task, Activity, File

# Create your views here.
@login_required
def my_tasks_view(request):
    user_tasks = Task.objects.filter(assigned_to=request.user).order_by('-created')
    if request.htmx:
        if 'table' in request.GET:
            return render(request, 'boostlab_tasks/tasks_snippet_table.html', {'user_tasks': user_tasks})
        elif 'manger_table' in request.GET:
            return render(request, 'boostlab_tasks/manager_task_table.html', {'user_tasks': user_tasks})
        elif 'manger_grid' in request.GET:
            return render(request, 'boostlab_tasks/manager_task_grid.html', {'user_tasks': user_tasks})
        else:
            return render(request, 'boostlab_tasks/tasks_snippet_grid.html', {'user_tasks': user_tasks})
    return render(request, 'boostlab_tasks/my_tasks.html', {'user_tasks': user_tasks})


def task_detail_view(request, pk):
    task = Task.objects.get(id=pk)
    return render(request, 'boostlab_tasks/task_detail.html', {'task': task})


@login_required
def task_create_view(request):
    form = TaskCreateForm()
    if request.method == 'POST':
        form = TaskCreateForm(request.POST,request.FILES)
        if form.is_valid():
            task=form.save(commit=False)
            task.manager=request.user.employee.manager
            task.save()
            # task.save_m2m()
            form.save_m2m()
            return redirect('task-detail', task.id)
    context={'form': form }
    return render(request, 'boostlab_tasks/task_create.html', context=context)


@login_required
def task_delete_view(request,pk):
    task = get_object_or_404(Task, id=pk, manager=request.user.employee.manager)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully')
        return redirect('my-tasks')
    context = {
        'task': task
    }
    return render(request, 'boostlab_tasks/task_delete.html', context=context)



@login_required
def task_edit_view(request,pk):
    task = get_object_or_404(Task, id=pk, manager=request.user.employee.manager)
    form =TaskEditForm(instance=task)
    if request.method == 'POST':
        form = TaskEditForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully')
            return redirect('task-detail', task.id)
    context = {
        'task': task,
        'form': form
    }

    return render(request, 'boostlab_tasks/task_edit.html', context=context)

@login_required
def activity_create_view(request,pk):
    task = get_object_or_404(Task, id=pk)
    form = ActivityCreateForm()
    if request.method == 'POST':
        form = ActivityCreateForm(request.POST,request.FILES)
        if form.is_valid():
            activity=form.save(commit=False)
            activity.participant=request.user
            activity.task=task
            activity.activity_file=request.FILES.get('activity_file')
            activity.save()
            # form.save_m2m()
            return redirect('task-detail', task.id)
    context={'form': form ,task: task}
    return render(request, 'boostlab_tasks/activity_create.html', context=context)


@login_required
def activity_delete_view(request,pk):
    activity = get_object_or_404(Activity, id=pk, participant=request.user)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully')
        return redirect('task-detail', activity.task.id)
    context = {
        'activity': activity
    }

    return render(request, 'boostlab_tasks/activity_delete.html', context=context)



@login_required
def file_create_view(request,pk):
    task = get_object_or_404(Task, id=pk)
    form = FileCreateForm()
    if request.method == 'POST':
        form = FileCreateForm(request.POST,request.FILES)
        if form.is_valid():
            file=form.save(commit=False)
            file.added_by=request.user
            file.task=task
            file.description=request.POST.get('description')
            file.file=request.FILES.get('file')
            file.save()
            # form.save_m2m()
            return redirect('task-detail', task.id)
    context={'form': form ,task: task}
    return render(request, 'boostlab_tasks/add_file.html', context=context)


@login_required
def file_delete_view(request,pk):
    file = get_object_or_404(File, id=pk, added_by=request.user)
    if request.method == 'POST':
        file.delete()
        messages.success(request, 'File deleted successfully')
        return redirect('task-detail', file.task.id)
    context = {
        'file': file
    }

    return render(request, 'boostlab_tasks/file_delete.html', context=context)