from django import forms
from sod.models import Module, File


class ModuleForm(forms.Form):
    name = forms.CharField(max_length=200, label="Название модуля")
    purpose = forms.ChoiceField(File.PURPOSE_CHOICES, label="Тип модуля")
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".py,.m,.exe"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))

    def save(self):
        print(self.files['file'])
        mod = Module(name=self.data['name'], purpose=self.data['purpose'], file=self.files['file'],
                     description=self.data['description'],
                     extension=str(self.files['file']).split('.')[-1])
        mod.save()
        print("THIS IS NOT PUNCHLINE")


class FileForm(forms.Form):
    name = forms.CharField(max_length=200, label="Название файла или списка файлов")
    purpose = forms.ChoiceField(File.PURPOSE_CHOICES, label="Тип файла")
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
