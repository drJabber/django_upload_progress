from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',view=views.hello,name='hello'),
    url(r'^parse/$',view=views.testPars,name='parse'),
    url(r'^upload/$',view=views.uploadFile,name='upload'),
    url(r'^list/$',view=views.listFiles,name='list'),
    url(r'^pict/$',view=views.loadPicture,name='pict'),
    
]
