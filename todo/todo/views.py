from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from todo.forms import TodoForm
from todo.models import Todo


def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).order_by('created_at')
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(title__icontains=q) | Q(description__icontains=q)
    paginator = Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'todo_list.html', context)


def todo_info(request, id):
    try:
        todo = Todo.objects.get(id=id)
        info = {
            'title': todo.title,
            'description': todo.description,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'is_complete': todo.is_complete,
        }
        return render(request, 'todo_info.html', {'data': info})
    except Todo.DoesNotExist:

        raise Http404("Todo does not exist")


# @login_required
# def todo_create(request):
#     form = TodoForm(request.POST or None)
#     if form.is_valid():
#         todo = form.save(commit=False)
#         todo.user = request.user
#         users.save()
#             return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))

