from django import forms
from django.db import IntegrityError

from escort.ocs.models import Task, SubTask
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class TaskForm(forms.Form):
    model_choices = [(x[0], x[1] + " " + x[2]) for x in
                     list(User.objects.all().values_list('id', 'first_name', 'last_name'))]

    name = forms.CharField(max_length=200, label='Заголовок задачи')
    description = forms.CharField(widget=forms.Textarea, label='Описание задачи')
    start_date = forms.DateField(label='Дата поступления задачи')
    deadline_date = forms.DateField(label='Срок окончания задачи')
    responsible = forms.ChoiceField(choices=model_choices, label="Ответственный")
    finish_rate = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def save(self):
        task = Task(name=self.cleaned_data['name'],
                    description=self.cleaned_data['description'],
                    start_date=self.cleaned_data['start_date'],
                    deadline_date=self.cleaned_data['deadline_date'],
                    responsible=User.objects.get(pk=int(self.cleaned_data['responsible'])),
                    finish_rate=self.cleaned_data['finish_rate'])
        try:
            task.save()
            return task
        except IntegrityError:
            self.add_error(field='name', error="Name already exist")
            # class Meta:
            #     # Создаем связь между ModelForm и моделью
            #     model = Task
            #     exclude = ()


class SubtaskForm(forms.Form):
    model_choices = [(x[0], x[1] + " " + x[2]) for x in
                     list(User.objects.all().values_list('id', 'first_name', 'last_name'))]

    name = forms.CharField(widget=forms.Textarea, label='Описание подзадачи')
    task = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    performers = forms.ChoiceField(choices=model_choices, label="Ответственный")

    def save(self):
        subtask = SubTask(
            name=self.cleaned_data['name'],
            is_finished=False,
        )
        subtask.save()
        subtask.task = Task.objects.get(pk=self.cleaned_data['task'])
        subtask.performer = [User.objects.get(pk=int(self.cleaned_data['performers']))]
        subtask.save()
        return subtask


class EditForm(forms.ModelForm):
    class Meta:
        # Создаем связь между ModelForm и моделью
        model = Task
        exclude = ()


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label='Логин пользователя',
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
    )
    first_name = forms.CharField(max_length=30, label='Имя пользователя')
    last_name = forms.CharField(max_length=30, label='Фамилия пользователя')
    is_superuser = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser')


class UserUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Имя пользователя')
    last_name = forms.CharField(max_length=30, label='Фамилия пользователя')
    email = forms.CharField(max_length=30, label='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class AdmUserUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Имя пользователя')
    last_name = forms.CharField(max_length=30, label='Фамилия пользователя')
    email = forms.CharField(max_length=30, label='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class GroupForm(forms.ModelForm):
    group_id = forms.CharField(max_length=1, label='группа')

    class Meta:
        model = Group
        fields = ('group_id',)
