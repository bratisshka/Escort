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

    # TODO Reformat code: add validators to field (Chapter 11)

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
    purpose = forms.ChoiceField(File.PURPOSE_CHOICES, label="Тип файла(ов)")
    modules = forms.ChoiceField(Module.objects.values_list('id', 'name'), widget=forms.SelectMultiple())
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
