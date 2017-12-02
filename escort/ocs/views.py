import os
import operator

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.templatetags.l10n import localize

from config.settings import PROJ_DIR
from escort.ocs.forms import *
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from escort.ocs.models import Task
from escort.ocs.cusdecorators import group_required
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table


@login_required
def index(request):
    my_tasks_list = Task.objects.filter(
        ~Q(finish_rate=100),
        ~Q(finish_rate=101),
        responsible_id=request.user.id
    ).order_by('finish_rate', 'deadline_date')
    list_of_subtask = SubTask.objects.order_by('is_finished')
    subtask_ref_list = [int(t[0]) for t in list(SubTask.objects.all().values_list('task_id'))]
    context_dict = {
        'tasks': my_tasks_list,
        'subtasks': list_of_subtask,
        'ref': subtask_ref_list,
    }
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
    list_of_tasks = Task.objects.filter(~Q(finish_rate=-1)).order_by('finish_rate', 'deadline_date')
    list_of_subtask = SubTask.objects.order_by('is_finished')
    subtask_ref_list = [int(t[0]) for t in list(SubTask.objects.all().values_list('task_id'))]
    context_dict = {
        'tasks': list_of_tasks,
        'subtasks': list_of_subtask,
        'ref': subtask_ref_list,
    }
    return render(request, 'ocs/task_list.html', context_dict)


@login_required
def show_task(request, task_id):
    context_dict = {}
    try:
        task = Task.objects.get(id=task_id)
        subtasks = SubTask.objects.filter(task_id=task_id)
        responsible = User.objects.get(id=task.responsible_id)
        a = SubTask.objects.all().values_list('performer')
        performers = [
            User.objects.get(id=perf_id) for perf_id in [
                int(t[0]) for t in list(SubTask.objects.all().values_list('performer'))
            ]
        ]
        subt_user = dict(zip(subtasks, performers))
        context_dict = {
            'task': task,
            'subtasks': subtasks,
            'responsible': responsible,
            'performers': performers,
            'subt_user': subt_user,
        }
    except Task.DoesNotExist:
        pass

    return render(request, 'ocs/show_task.html', context_dict)


@login_required
def subtask_done(request, subtask_id):
    # refresh subtask
    subtask = SubTask.objects.get(id=subtask_id)
    subtask.is_finished = 1
    subtask.save()
    # refresh task
    task = Task.objects.get(id=subtask.task_id)
    subt_count = len(list(SubTask.objects.filter(task_id=task.id)))
    done_subt_count = len(list(SubTask.objects.filter(
        task_id=task.id,
        is_finished=1,
    )))
    if subt_count == done_subt_count:
        task.finish_rate = 99
    else:
        task.finish_rate = int(done_subt_count * 100 / subt_count)
    task.save()
    return redirect('/ocs/show_task/' + str(subtask.task_id))


@login_required
def task_chek(request, task_id):
    task = Task.objects.get(id=task_id)
    task.finish_rate = 100
    task.save()
    return redirect('/ocs/show_task/' + str(task_id))


@login_required
def task_fail(request, task_id):
    task = Task.objects.get(id=task_id)
    task.finish_rate = 101
    task.save()
    return redirect('/ocs/show_task/' + str(task_id))


@login_required
def delete_task(request, task_id):
    u = Task.objects.get(id=task_id)
    u.delete()
    return redirect('/ocs/task_list/')


@login_required
@group_required('Admins')
def edit_task(request, task_id):
    instance = get_object_or_404(Task, id=task_id)
    form = EditForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('next_view')
        # return direct_to_template(request, 'my_template.html', {'form': form}


@login_required
def statistic(request):
    tasks = Task.objects.all()
    users_count = len(User.objects.all())
    adm_count = len(User.objects.filter(is_superuser=1))
    done_task = Task.objects.filter(finish_rate=100)
    fail_task = Task.objects.filter(finish_rate=101)
    wait_task = Task.objects.filter(finish_rate=99)
    work_task = Task.objects.filter(finish_rate__lte=98)

    context_dict = {
        'tasks': tasks,
        'done_task': done_task,
        'fail_task': fail_task,
        'wait_task': wait_task,
        'work_task': work_task,
        'users_count': users_count,
        'adm_count': adm_count,
    }
    return render(request, 'ocs/statistic.html', context_dict)


# Statistic charts
def statistic_donat(request):
    tasks = Task.objects.all()
    fail_task = Task.objects.filter(finish_rate=101)
    wait_task = Task.objects.filter(finish_rate=99)
    work_task = Task.objects.filter(finish_rate__lte=98)

    fail_task_pers = int(len(fail_task) * 100 / len(tasks))
    wait_task_pers = int(len(wait_task) * 100 / len(tasks))
    work_task_pers = int(len(work_task) * 100 / len(tasks))
    done_task_pers = 100 - (fail_task_pers + wait_task_pers + work_task_pers)

    response_data = [{"label": "Провалено", "value": fail_task_pers},
                     {"label": "Ожидает подтверждения", "value": wait_task_pers},
                     {"label": "Выполняется", "value": work_task_pers},
                     {"label": "Выполнено", "value": done_task_pers}]
    # serialized_data = serializers.serialize('json', response_data)
    # return HttpResponse(json.dumps(response_data), content_type="application/json")
    return JsonResponse(response_data, safe=False)


def statistic_bar(requset):
    response_data = [{"x": user.last_name,
                      "y": len(Task.objects.filter(finish_rate=100, responsible=user))} for user in User.objects.all()]

    return JsonResponse(response_data, safe=False)


@login_required
@group_required('Admins')
def report(request):

    return render(request, 'ocs/report.html')


def report_generate(request):
    # data for including in report
    tasks = Task.objects.all()
    done_task = Task.objects.filter(finish_rate=100)
    fail_task = Task.objects.filter(finish_rate=101)
    wait_task = Task.objects.filter(finish_rate=99)
    work_task = Task.objects.filter(finish_rate__lte=98)

    done_task_pers = int(len(done_task) * 100 / len(tasks))

    user_stat = [(user, len(Task.objects.filter(finish_rate=100, responsible=user))) for user in User.objects.all()]
    user_stat.sort(key=lambda x: -x[1])

    top_count = i = 3
    while (user_stat[i-1][1] == user_stat[i][1]) & (i < len(user_stat)):
        top_count += 1
        i += 1

    # report generation
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="somereport.pdf"'  # download
    response['Content-Disposition'] = 'filename="somereport.pdf"'  # preview
    p = canvas.Canvas(response)
    today = localize(datetime.now().date())

    # отрисовка PDF
    p.setLineWidth(.3)
    # Register font family
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

    # cap
    p.drawImage(os.path.abspath(os.path.join(str(PROJ_DIR), "static/ocs/images/pdf_logo.png")),
                80, 740,
                width=115,
                height=35,
                )
    p.setFont("Verdana", 11)
    p.drawString(450, 765, 'АИС "Эскорт"')
    p.drawString(377, 750, 'Система контроля работы')

    # header
    p.setFont("Verdana", 14)
    p.drawString(286, 630, 'ОТЧЕТ')

    # body
    p.setFont("Verdana", 12)
    p.drawString(120, 580, 'На момент ' + today + ' в аналитический центр поступило')
    p.drawString(80, 560, str(len(tasks))
                 + ' задач.  Из них было выполнено в срок: '
                 + str(len(done_task))
                 + '; ожидают подтверждения')
    p.drawString(80, 540, 'о выполнении: '
                 + str(len(wait_task))
                 + '; находятся на стадии выполнения: '
                 + str(len(work_task))
                 + '; по каким-либо')
    p.drawString(80, 520, 'причинам не выполнено: '
                 + str(len(fail_task))
                 + '.')
    p.drawString(120, 490, 'Итого, аналитический цетр решил '
                 + str(done_task_pers)
                 + '% поставленных на момент')
    p.drawString(80, 470, 'составления отчета задач.')
    p.drawString(120, 440, 'Наибольшее число задач решили следующие сотрудники:')

    iter = 0
    for user in user_stat[0:top_count]:
        p.drawString(140, 415 - iter, '• '
                     + str(user[0].last_name) + ' '
                     + str(user[0].first_name) + ' '
                     + '(решенных задач: '
                     + str(user[1]) + ')')
        iter += 20

    # table
    # p.setLineWidth(.9)
    # p.line(80, 430, 530, 430)


    # footer
    p.drawString(80, 170, 'Начальник аналитического центра')
    p.drawString(80, 145, 'рядовой')
    p.line(200, 145, 400, 145)
    p.drawString(450, 145, 'Р.В. Никонов')
    p.setFont("Verdana", 8)
    p.drawString(280, 135, '(подпись)')
    p.setFont("Verdana", 11)
    p.drawString(80, 120, today)
    p.showPage()
    p.save()

    return response


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
        user = AdmUserUpForm(request.POST, instance=inst_user)
        if user.is_valid():
            user.save()
            return redirect('/ocs/users_list/')
    else:
        inst_user = User.objects.get(id=user_id)
        user = AdmUserUpForm(instance=inst_user)
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
