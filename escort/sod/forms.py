from django import forms
from django.db import IntegrityError

from .models import Module, File
from .validators import find_module_extension


class ModuleForm(forms.Form):
    name = forms.CharField(max_length=200, label="Название модуля")
    purpose = forms.ChoiceField(File.PURPOSE_CHOICES, label="Тип модуля")
    # extension = forms.ChoiceField(Module.EXTENSION_CHOICES,
    #                               label="Тип исполняемого файла") # не нужно, находим start.py
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))

    def save(self):
        mod = Module(name=self.data['name'],
                     purpose=self.data['purpose'],
                     description=self.data['description'],
                     extension=self.find_module_extension())
        try:
            mod.save()
            mod.make_module_directory(self.files.getlist('file'))
            return mod
        except IntegrityError:
            self.add_error(field='name', error="Name already exist")

    def find_module_extension(self):
        """
        Добавление валидаторов в поле не работает, потому что посылается в него только один файл из несколькких
        """
        files = self.files.getlist('file')
        for file in files:
            if file.name.split('.')[0] == "start":
                ext = file.name.split('.')[1]
                if ext in Module.SUPPORTED_EXTENSIONS:
                    return ext
        self.add_error(field='file', error="Couldn't find start file")
        return None

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        self.extension = self.find_module_extension()
        valid = self.extension is not None
        return valid

    class Meta:
        model = Module


class FileForm(forms.Form):
    module_choices = list(Module.objects.filter(is_service=False).values_list('id', 'name'))
    module_choices.append((0, "Входящий поток"))
    module = forms.ChoiceField(choices=module_choices, initial=0)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def save(self):
        module_id = self.data.get('module', 0)
        if module_id == 0:
            pass
            # TODO вызвать распределяющий модуль
        try:
            mod = Module.objects.get(pk=module_id)
            files = self.files.getlist('file_field')
            mod.append_to_input(files)
        except Module.DoesNotExist:
            self.add_error(field='module', error='Module does not exist')
