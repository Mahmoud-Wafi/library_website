from django.shortcuts import render, get_object_or_404, redirect
from .forms import adddbook
from .models import Book, Borrow
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from account.models import Students
# Create your views here.
def index(request):
    context = {"book":Book.objects.all()}
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')

def books(request):
    bro = Book.objects.all()
    context = {"bro": bro}
    return render(request, 'pages/books.html', context)

def book(request, id):
    bro = get_object_or_404(Book, pk = id)
    context = {"bro":bro}
    return render(request, 'pages/bookdetails.html', context)


def addbookform(request):
    if request.user.is_authenticated and request.user.is_superuser:
        name = None
        author = None
        description = None
        price = None
        category = None
        photo = None
        
        if 'name' in request.GET: name = request.GET['name']
        
        if 'author' in request.GET: author = request.GET['author']
        
        if 'description' in request.GET: description = request.GET['description']
     
        if 'price' in request.GET: price = request.GET['price']
        
        if 'category' in request.GET: category = request.GET['category']
        
        if 'photo' in request.GET: photo = request.GET['photo']
        
        if name and author and description and price and category and photo:
            addbo = Book(name=name, author=author, description=description, price=price, category=category, photo=photo)
            addbo.save()
            
            messages.success(request, 'Book is created')
            
        else:
            messages.error(request, 'check empty fields')
        return render(request, 'pages/addbook.html')
    else:
        return render(request, 'pages/addbook.html')
    
def editbook(request, id):
    if request.GET and "btnupdate" in request.GET:
        if request.GET['name'] and request.GET['author'] and request.GET['description'] and request.GET['price'] and request.GET['category'] and request.GET['photo']:
            pro = Book.objects.get(pk = id)
            pro.name = request.GET['name']
            pro.author = request.GET['author']
            pro.description = request.GET['description']
            pro.price = request.GET['price']
            pro.category = request.GET['category']
            pro.photo = request.GET['photo']
            pro.save()
            messages.success(request, 'Book is updated')
        else:
            messages.error(request, "check your values!")
        return redirect("books")
    else:
        if request.method == "GET":
            pro = get_object_or_404(Book, pk = id)
            context = {"pro":pro}
            return render(request, 'pages/editbook.html', context)
    return redirect("books")
            


def addborrow(request, id):
    book = Book.objects.get(id=id)
    student = Students.objects.get(user = request.user)
    if request.user.is_authenticated:
        if Borrow.objects.filter(book=book).exists():
            messages.info(request, "This book is already borrowed.")
            return redirect("/" + str(id))
        else:
            borr = Borrow(student=student, book=book)
            borr.save()
            messages.success(request, "The book has been borrowed")
            return redirect("/" + str(id))
    else:
        return redirect("index")
        
    

def deletebook(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        pro = get_object_or_404(Book, pk = id)
        pro.delete()
        return redirect("books")
    else:
        return redirect("index")
    
def showborrbook(request):
    context = None
    if request.user.is_authenticated:
        student = Students.objects.get(user = request.user)
        if Borrow.objects.filter(student=student):
            borr = Borrow.objects.get(student=student)
            context={"borr":borr}
            return render(request, 'pages/borrow.html', context)
        else:
            return redirect("index")
    else:
        return redirect("index")
    
def delborrbook(request, id):
    if request.user.is_authenticated:
        pro = get_object_or_404(Borrow, pk=id)
        pro.delete()
        return redirect("books")
    else:
        return redirect("index")
    
def adminshborrow(request):
    if request.user.is_authenticated and request.user.is_superuser:
        borr = Borrow.objects.all()
        context = {"borr":borr}
        return render(request, 'pages/adminborrow.html', context)
    else:
        return redirect("index")