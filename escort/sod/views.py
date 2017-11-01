from django.http import HttpResponse
from django.shortcuts import render
from .forms import ModuleForm, FileForm

# Create your views here.
from .models import Module


def index(request):
    return render(request, 'sod/index.html')


def matlab(request):
    return render(request, 'sod/matlab.html')


def python(request):
    return render(request, 'sod/python.html')


def exe(request):
    return render(request, 'sod/exe.html')


def add_module(request):
    form = ModuleForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            HttpResponse("Заебись")
        print('Done')
    return render(request, 'sod/add_module.html', {'form': form})


def add_files(request):
    # if request.method == 'POST':
    #     form = FileForm(request.POST, request.FILES)
    form = FileForm(request.POST or None, request.FILES or None)
    return render(request, 'sod/add_files.html', {'form': form})


def run_module(request):
    return render(request, 'sod/run_module.html')


def all_modules(request):
    modules = Module.objects.all()
    return render(request, 'sod/all_modules.html', {'modules': modules})
