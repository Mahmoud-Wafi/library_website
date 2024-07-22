from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('about/', views.about, name ="about"),
    path('books/', views.books, name= 'books'),
    path('<int:id>', views.book, name= 'book'),
    path('addbook/', views.addbookform, name= 'addbookform'),
    path('editbook/<int:id>', views.editbook, name = "edbook"),
    path('deletebook/<int:id>', views.deletebook, name = "delbook"),
    path('addborrow/<int:id>', views.addborrow, name = "borrbook"),
    path('showborrow/', views.showborrbook, name= "showborrow"),
    path('delborrow/<int:id>', views.delborrbook, name = "delborrow"),
    path('adminshowborrow/', views.adminshborrow, name = "adminshowborrow")
]
