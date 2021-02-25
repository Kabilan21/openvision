from django.urls import path
from . import views
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('add/user', views.adduser, name='addUser'),
    path('update/user', views.updatesystem, name='updatesystem'),
    path('start/system', views.startsystem, name='startsystem'),
    path('stop/system', views.stopsystem, name='stopsystem'),
]
