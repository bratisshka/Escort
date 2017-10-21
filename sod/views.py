from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'sod/index.html')


def matlab(request):
    return render(request, 'sod/matlab.html')


def python(request):
    return render(request, 'sod/python.html')


def exe(request):
    return render(request, 'sod/exe.html')


def add_module(request):
    return render(request, 'sod/add_module.html')


def add_files(request):
    return render(request, 'sod/add_files.html')


def run_module(request):
    return render(request, 'sod/run_module.html')