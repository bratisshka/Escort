import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, View, ListView
from .common.manager import ModuleManager
from .forms import ModuleForm, FileForm

# Create your views here.
from .models import Module


def index(request):
    return render(request, "sod/index.html")


def matlab(request):
    return render(request, 'sod/matlab.html')


def python(request):
    return render(request, 'sod/python.html')


def exe(request):
    return render(request, 'sod/exe.html')


@login_required
def add_files(request):
    form = FileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.data['module'] != 0:
            module = get_object_or_404(Module, pk=form.data['module'])
            form.save()
            return redirect(module.get_absolute_url())
        else:
            form.save()
    return render(request, 'sod/add_files.html', {'form': form})


class AddFilesToModuleView(View):
    @login_required
    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        form.save()
        return JsonResponse({"success": True})


class AddModuleView(View):
    form_class = ModuleForm
    template_name = 'sod/add_module.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=None)
        return render(request, self.template_name, {'form': form})

    @login_required
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            mod = form.save()
            return redirect(mod.get_absolute_url())
        return render(request, self.template_name, {'form': form})


@login_required
def run_module(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if module.state == module.STOPPED:
        ModuleManager.run_module(module.id)
    return redirect(module.get_absolute_url())


@login_required
@require_POST
def clear_module_input_dir(request, pk):
    module = get_object_or_404(Module, pk=pk)
    ModuleManager.clean_input_data(module.id)
    return HttpResponse("Очищено")


@login_required
@require_POST
def clear_module_output_dir(request, pk):
    module = get_object_or_404(Module, pk=pk)
    ModuleManager.clean_output_data(module.id)
    return HttpResponse("Очищено")


@login_required
def show_module_directory(request, pk):  # NOT WORKING
    module = get_object_or_404(Module, pk=pk)
    filelist = os.listdir(str(module.get_module_directory()))
    context = {
        "data": "\n".join(filelist)
    }
    return JsonResponse(context)


@login_required()
def download_out_zip(request, pk):
    from wsgiref.util import FileWrapper

    mod = get_object_or_404(Module, pk=pk)
    archive, name = ModuleManager.make_out_archive(mod.id)
    try:
        archive = open(archive, 'rb')
        response = HttpResponse(FileWrapper(archive), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename={}'.format(name)
    except FileNotFoundError:
        raise Http404("File does not exist")
    finally:
        archive.close()
    return response


class AllModulesView(ListView):
    # model = Module
    template_name = 'sod/all_modules.html'
    context_object_name = 'modules'

    def get_queryset(self):
        return Module.objects.filter(is_service=False)


class ModuleView(DetailView):
    model = Module
    template_name = 'sod/module_detail.html'
    context_object_name = 'module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def module_view(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if module.id == 1:
        return redirect('/sod/')
    else:
        return render(request, 'sod/module_detail.html', {'module': module})


@login_required
def show_log(request, pk):
    mod = get_object_or_404(Module, pk=pk)
    log = mod.show_log_file()
    return JsonResponse({"data": log})


@login_required
def show_out(request, pk):
    mod = get_object_or_404(Module, pk=pk)
    out = mod.show_output_file()
    return JsonResponse({"data": out})
