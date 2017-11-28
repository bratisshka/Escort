from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from escort.ocs.forms import *
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from escort.ocs.models import Task
from escort.ocs.cusdecorators import group_required
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    my_tasks_list = Task.objects.filter(
        ~Q(finish_rate=100),
        responsible_id=request.user.id
    ).order_by('finish_rate', 'deadline_date')
    context_dict = {'tasks': my_tasks_list}
    return render(request, 'ocs/index.html', context_dict)


@login_required
@group_required('Admins')
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        is_subtasks = request.POST.get('subtasks', 0)
        if form.is_valid():
            task = form.save()
            if is_subtasks:
                return HttpResponse(task.id)
            return index(request)
        else:
            print(form.errors)
    else:
        form = TaskForm()
    users = User.objects.all()
    return render(request, 'ocs/add_task.html', {'form': form, 'users': users})


@login_required
@group_required('Admins')
def add_subtask(request):
    form = SubtaskForm(request.POST or None)
    count = request.GET.get('count', 0)
    users = User.objects.all()
    if request.method == "POST":
        form = SubtaskForm(request.POST)
        if form.is_valid():
            subtask = form.save()
            return HttpResponse("OK")
        else:
            return HttpResponse("BAD")
    return render(request, 'ocs/add_subtask.html', {'form': form, 'users': users, 'count': count})


@login_required
def task_list(request):
    list_of_tasks = Task.objects.order_by('finish_rate', 'deadline_date')
    context_dict = {'tasks': list_of_tasks}
    return render(request, 'ocs/task_list.html', context_dict)


@login_required
def show_task(request, task_id):
    context_dict = {}

    try:
        task = Task.objects.get(id=task_id)
        context_dict['task_name'] = task.name
        context_dict['task_description'] = task.description
        context_dict['start_date'] = task.start_date
        context_dict['deadline_date'] = task.deadline_date
        context_dict['responsible'] = task.responsible
        context_dict['finish_rate'] = task.finish_rate

    except Task.DoesNotExist:
        pass

    return render(request, 'ocs/task_details.html', context_dict)


@login_required
@group_required('Admins')
def edit_task(request, task_id):
    instance = get_object_or_404(Task, id=task_id)
    form = EditForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('next_view')
        # return direct_to_template(request, 'my_template.html', {'form': form}


# Operation with users
def accounts(request):
    return render(request, "registration/profile_control.html")


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        group_form = GroupForm(request.POST)
        if user_form.is_valid() and group_form.is_valid():
            # Get group id
            g_id = group_form.cleaned_data.get('group_id')
            # if g_id == '1':
            #     user_form.cleaned_data['is_superuser'] = True
            user_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # Add user in group
            g = Group.objects.get(id=g_id)
            g.user_set.add(user)
            return redirect('/ocs/users_list')
    else:
        user_form = SignUpForm()
        group_form = GroupForm()
    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'group_form': group_form
    })


@login_required
def profile_control(request):
    if request.method == 'POST':
        user = UserUpForm(request.POST, instance=request.user)
        if user.is_valid():
            user.save()
            return redirect('/ocs/')
        login(request, user)
    else:
        user = UserUpForm(instance=request.user)
    return render(request, "registration/profile_control.html", {
        'user': user,
    })


@login_required
@group_required('Admins')
def adm_profile_control(request, user_id):
    if request.method == 'POST':
        inst_user = User.objects.get(id=user_id)
        user = UserUpForm(request.POST, instance=inst_user)
        if user.is_valid():
            user.save()
            return redirect('/ocs/users_list/')
    else:
        inst_user = User.objects.get(id=user_id)
        user = UserUpForm(instance=inst_user)
    return render(request, "registration/profile_control.html", {
        'user': user,
    })


@login_required
@group_required('Admins')
def del_user(request, user_id):
    u = User.objects.get(id=user_id)
    u.delete()
    return redirect('/ocs/users_list/')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/ocs/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


@login_required
@group_required('Admins')
def users_list(request):
    list_of_users = User.objects.order_by('last_name', 'first_name')
    context_dict = {'users': list_of_users}
    return render(request, 'registration/users_list.html', context_dict)
