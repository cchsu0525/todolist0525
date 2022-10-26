from django.shortcuts import redirect,render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserForm

@login_required
def user_logout(request):
    logout(request)
    return redirect('todo')

@login_required
def profile(request):
    return render(request,'./user/profile.html')

def user_login(request):
    message,username='',''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        if username=='' or password=='':
            message='帳號與密碼不能為空!'
        else:
            user=authenticate(request,username=username,password=password)
            if user is None:
                if User.objects.filter(username=username):
                    message='密碼有誤'
                else:
                    message='帳號有誤'
            else:
                login(request,user)
                message='登入中...'     
                return redirect('todo')       


        if request.POST.get('login'):
            print('login')
        elif request.POST.get('register'):    
            return redirect('register')
        
    return render(request,'./user/login.html',{'message':message})


# Create your views here.
def user_register(request):

    #form=UserCreationForm()
    form=MyUserForm()
    message=''
    # print(User.objects.all())

    # for user in User.objects.all():
    #     print(user.id,user.username,user.email)

    if request.method=='GET':
        print('GET')
    elif request.method=='POST':
        print('POST')
        print(request.POST)    
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')

        if len(password1)<8:
            message='密碼少於8個字元'
        elif password1!=password2:
            message='兩次密碼不同'  
        else:
            if User.objects.filter(username=username).exists():
                message='帳號重複'
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.save()
                message='註冊成功'  
                login(request,user)
                return redirect('profile')    

    return render(request,'./user/register.html',{'form':form,'message':message})