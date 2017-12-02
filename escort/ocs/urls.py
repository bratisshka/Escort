from django.conf.urls import url

from . import views

app_name = 'ocs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # operation with users
    url(r'^profile_control/$', views.profile_control, name='profile_control'),
    url(r'^adm_profile_control/(?P<user_id>[\w\-]+)/$', views.adm_profile_control, name='adm_profile_control'),
    url(r'^del_user/(?P<user_id>[\w\-]+)/$', views.del_user, name='del_user'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^users_list/$', views.users_list, name='users_list'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^signup/$', views.signup, name='signup'),
    # operation with tasks
    url(r'^add_task/$', views.add_task, name='add_task'),
    url(r'^add_subtask/$', views.add_subtask, name='add_subtask'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^show_task/(?P<task_id>[\w\-]+)/$', views.show_task, name='show_task'),
    url(r'^edit_task/(?P<task_id>[\w\-]+)/$', views.edit_task, name='edit_task'),
    url(r'^subtask_done/(?P<subtask_id>[\w\-]+)/$', views.subtask_done, name='subtask_done'),
    url(r'^task_chek/(?P<task_id>[\w\-]+)/$', views.task_chek, name='task_chek'),
    url(r'^task_fail/(?P<task_id>[\w\-]+)/$', views.task_fail, name='task_fail'),
    url(r'^delete_task/(?P<task_id>[\w\-]+)/$', views.delete_task, name='delete_task'),
    url(r'^statistic/$', views.statistic, name='statistic'),
    url(r'^statistic_donat/$', views.statistic_donat, name='statistic_donat'),
    url(r'^statistic_bar/$', views.statistic_bar, name='statistic_bar'),
    url(r'^report/$', views.report, name='report'),
    url(r'^report_generate/$', views.report_generate, name='report_generate'),
]
