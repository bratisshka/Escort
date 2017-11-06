from django.core.exceptions import ValidationError

from .models import Module


def find_module_extension(files):
    print(files)
    # files = self.files.getlist('file')
    # for file in files:
    file = files
    if file.name.split('.')[0] == "start":
        ext = file.name.split('.')[1]
        if ext in Module.SUPPORTED_EXTENSIONS:
            return None
    # self.add_error(field='file', error="Couldn't find start file")
    raise ValidationError("Can't find start file")
    # return None
