from django.conf.urls import url

from escort.app import views

app_name = 'app'
urlpatterns = [
    url(r'^news/$', views.news, name='news'),
    url(r'^documents/$', views.documents, name='documents'),
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^videos/$', views.videos, name='videos'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^map/$', views.map, name='map'),
    url(r'^center/$', views.center, name='center'),
    url(r'^$', views.index, name='index')
]