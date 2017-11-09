from django.conf.urls import url

from . import views

app_name = 'sod'
urlpatterns = [
    url(r'^matltab/$', views.matlab, name='matlab'),
    url(r'^python/$', views.python, name='python'),
    url(r'^exe/$', views.exe, name='exe'),
    url(r'^module/(?P<pk>[0-9]+)/$', views.ModuleView.as_view(), name='module'),
    url(r'^module/(?P<pk>[0-9]+)/clean_input/$', views.clear_module_input_dir, name='clean_module_input'),  # DRY
    url(r'^module/(?P<pk>[0-9]+)/clean_output/$', views.clear_module_output_dir, name='clean_module_output'),
    url(r'^module/(?P<pk>[0-9]+)/show_dir/$', views.show_module_directory, name='show_dir'),
    url(r'^module/(?P<pk>[0-9]+)/download_out/$', views.download_out_zip, name='download_output'),
    url(r'^module/(?P<pk>[0-9]+)/run_module/$', views.run_module, name='run_module'),
    url(r'^add_module/$', views.AddModuleView.as_view(), name='add_module'),
    url(r'^add_files/$', views.add_files, name='add_files'),
    url(r'^add_files_to_module/$', views.AddFilesToModuleView.as_view(), name='add_files_to_module'),
    url(r'^all_modules/$', views.AllModulesView.as_view(), name='all_modules'),
    url(r'^$', views.index, name='index'),
]
