from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from todo.forms import TodoForm, TodoUpdateForm
from todo.models import Todo


def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).order_by('created_at')
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(Q(title__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'todo_list.html', context)


# 추후 확인!
@login_required()
def todo_info(request, id):
    todo = get_object_or_404(Todo, id=id)
    context = {
        'todo': todo.__dict__
    }
    return render(request, 'todo_info.html', context)


@login_required
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs={'id': todo.pk}))
    context = {
        'form': form
    }
    return render(request, 'todo/todo_create.html', context)


def todo_update(request, id):
    todo = get_object_or_404(Todo, user=request.user, id=id)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        todo.save()
        return redirect(reverse('todo_info', kwargs={'id': todo.pk}))
    context = {
        'form': form,
    }
    return render(request, 'todo/todo_update.html', context)


@login_required()
def todo_delete(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))
