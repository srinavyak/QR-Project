from webapi import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('updateprofile', views.updateprofile, name='updateprofile'),
    path('template', views.template, name='template'),
    path('templateform', views.templateform, name='templateform'),
    path('tempform', views.tempform, name='tempform'),
    path('formdata', views.formdata, name='formdata'),
    # path('generaterow', views.generaterow, name='generaterow'),
    # path('dropdown', views.dropdown, name='dropdown'),
    path('formdetails', views.formdetails, name='formdetails'),
    path('docupload', views.docupload, name='docupload'),
    path('fileinsert', views.fileinsert, name='fileinsert'),
    path('fileview', views.fileview, name='fileview'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('userchangepassword', views.userchangepassword, name='userchangepassword'),
    path('changepassword1', views.changepassword1, name='changepassword1'),
    path('adduser', views.adduser, name='adduser'),
    path('adduser1', views.adduser1, name='adduser1'),
    path('userform', views.userform, name='userform'),
    path('userform1', views.userform1, name='userform1'),
    path('userdetails', views.userdetails, name='userdetails'),
    path('userdetails1', views.userdetails1, name='userdetails1'),
    path('getid', views.getid, name='getid'),
    path('getusertypeid', views.getusertypeid, name='getusertypeid'),
    path('gettemid', views.gettemid, name='gettemid'),
]