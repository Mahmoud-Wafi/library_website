from django.urls import path
from . import views

urlpatterns = [
    path('stdsignup/', views.studentsignup, name ="stdsignup"),
    path('stdsignin/', views.studentsignin, name ="stdsignin"),
    path('stdprofile/', views.studentprofile, name= "stdprofile"),
    path('logout/', views.logout, name = "log_out"),
    path('adminsignin/', views.adminsignin, name = "adminsignin"),
    path('stdsprofile/', views.stdsprofile, name= "stdspro")
]
