from django.conf.urls import url

from . import views

app_name = 'apigui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^files/$', views.files, name='files'),
    url(r'^apikey/$', views.apikey, name='apikey'),
    url(r'^apikey/edit', views.edit_apikey, name='edit_apikey'),
    url(r'^info/$', views.info, name='info'),
    url(r'^tasks/$', views.scheduled_tasks, name='tasks'),
    url(r'^destroy/$', views.destroy, name='destroy'),

]
