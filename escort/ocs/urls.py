from django.conf.urls import url

from . import views

app_name = 'ocs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile_control/$', views.profile_control, name='profile_control'),
    url(r'^adm_profile_control/(?P<user_id>[\w\-]+)/$', views.adm_profile_control, name='adm_profile_control'),
    url(r'^del_user/(?P<user_id>[\w\-]+)/$', views.del_user, name='del_user'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^users_list/$', views.users_list, name='users_list'),
    url(r'^add_task/$', views.add_task, name='add_task'),
    url(r'^add_subtask/$', views.add_subtask, name='add_subtask'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^show_task/(?P<task_id>[\w\-]+)/$', views.show_task, name='show_task'),
    url(r'^edit_task/(?P<task_id>[\w\-]+)/$', views.edit_task, name='edit_task'),
    url(r'^signup/$', views.signup, name='signup'),
]
