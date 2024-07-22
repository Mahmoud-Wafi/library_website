from django.shortcuts import redirect, render
from .models import Students
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
import re
# Create your views here.
def studentsignup(request):
    if request.POST and 'btnsignup' in request.POST:
        #variables for fields
        fname = None
        lname = None
        email = None
        phone = None
        photo = None
        username = None
        password = None
        is_added= None
        #Get Values From The Form
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in first name')
        
        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in last name')
        
        
        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in email')
        
        if 'phone' in request.POST: phone = request.POST['phone']
        else: messages.error(request, 'Error in phone')
        
        if 'photo' in request.POST: photo = request.POST['photo']
        else: messages.error(request, 'Error in photo')
        
        if 'username' in request.POST: username = request.POST['username']
        else: messages.error(request, 'Error in username')
        
        if 'password' in request.POST: password = request.POST['password']
        else: messages.error(request, 'Error in password')
        
        #Check the values 
        
        if fname and lname and email and phone and photo  and username and password:
            
                #check if username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This username is taken')
                else:
                    #check if email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is taken')
                    else:
                        patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt, email):
                            #add user
                            user = User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=password,)
                            user.save()
                            userstd = Students(user = user, phone = phone, photo = photo)
                            userstd.save()
                            #clear fields
                            fname = ''
                            lname = ''
                            email = ''
                            phone = ''
                            photo = ''
                            username = ''
                            password = ''
                            #success message
                            messages.success(request, 'Your account is created')
                            is_added = True                     
                        else:
                            messages.error(request, 'Invalid Email')
                
        else:
            messages.error(request, 'check empty fields')
        return render(request, 'accounts/signupstd.html', {
            'fname':fname,
            'lname':lname,
            'email':email,
            'phone':phone,
            'photo':photo,
            'user':username,
            'pass':password,
            'is_added':is_added,
        })
    else:
        return render(request, 'accounts/signupstd.html')
    
    
def studentsignin(request):
    if request.POST and 'btnlogin' in request.POST:
        username = None
        password = None
        if 'username' in request.POST: username = request.POST['username']
        else: messages.error(request, 'Error in username')
        
        if 'password' in request.POST: password = request.POST['password']
        else: messages.error(request, 'Error in password')
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if 'rememberme' not in request.POST:
                    request.session.set_expiry(0)
                auth.login(request, user)
                #messages.success(request, 'You are now logged in')
            else:
                messages.error(request, 'username or password invalid')
        else:
            messages.error(request, 'check empty fields')
        return redirect('stdsignin')
    else:
        return render(request, 'accounts/signinstd.html')
    
def studentprofile(request):
    if request.POST and "btnsave" in request.POST:
        if request.user is not None and request.user.id != None:
            userprofile = Students.objects.get(user=request.user)
            if (
                request.POST["fname"] 
                and request.POST["lname"] 
                and request.POST["email"]
                and request.POST["phone"]
                and request.POST["photo"]
                and request.POST["username"]
                and request.POST["password"]
            ):
                request.user.first_name = request.POST["fname"]
                request.user.last_name = request.POST["lname"]
                request.user.email = request.POST["email"]
                userprofile.phone = request.POST["phone"]
                userprofile.photo = request.POST["photo"]
                if not request.POST["password"].startswith("pbkdf2_sha256$"):
                    request.user.set_password(request.POST["pass"])
                request.user.save()
                userprofile.save()
                auth.login(request, request.user)
                messages.success(request, "Your data has been saved")
            else:
                messages.error(request, "check your values!")
        return redirect("stdprofile")
    else:
        if request.user is not None:
            context = None
            if not request.user.is_anonymous:
                userprofile = Students.objects.get(user=request.user)
                context = {
                    "fname": request.user.first_name,
                    "lname": request.user.last_name,
                    "email": request.user.email,
                    "phone": userprofile.phone,
                    "photo": userprofile.photo,
                    "username": request.user.username,
                    "password": request.user.password,
                }
            return render(request, "accounts/profilestd.html", context)
        else:
            return redirect("stdprofile")
        
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect("index")
    
def adminsignin(request):
    if request.POST and 'btnlogin' in request.POST:
        username = None
        password = None
        if 'username' in request.POST: username = request.POST['username']
        else: messages.error(request, 'Error in username')
        
        if 'password' in request.POST: password = request.POST['password']
        else: messages.error(request, 'Error in password')
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if 'rememberme' not in request.POST:
                    request.session.set_expiry(0)
                auth.login(request, user)
                #messages.success(request, 'You are now logged in')
            else:
                messages.error(request, 'username or password invalid')
        else:
            messages.error(request, 'check empty fields')
        return redirect('adminsignin')
    else:
        return render(request, 'accounts/signinadmin.html')
    
def stdsprofile(request):
    pro = Students.objects.all()
    pro_id = None
    if 'searchname' in request.GET and request.user.is_superuser:
            pro_id = request.GET["searchname"]
            pro = pro.filter(id__icontains = pro_id)
            
    
    context = {"pro": pro}
    return render(request, 'accounts/studentsprofile.html', context)
    