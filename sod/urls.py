from django.conf.urls import url

from sod import views

app_name = 'sod'
urlpatterns = [
    url(r'matltab/$', views.matlab, name='matlab'),
    url(r'python/$', views.python, name='python'),
    url(r'exe/$', views.exe, name='exe'),
    url(r'add_module/$', views.add_module, name='add_module'),
    url(r'add_files/$', views.add_files, name='add_files'),
    url(r'run_module/$', views.run_module, name='run_module'),
    url(r'$', views.index, name='index'),
]
