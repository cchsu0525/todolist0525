from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Todo
from .forms import TodoForm
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def completed_by_id(request,id):
    todo=Todo.objects.get(id=id)
    todo.completed=not todo.completed
    todo.date_complated=datetime.now() if todo.completed else None
    todo.save()
    return redirect('todo')

@login_required
def delete(request,id):
    todo=Todo.objects.get(id=id)
    todo.delete()
    return redirect('todo')

@login_required
def completed(request):
    # 篩選已完成項目
    todos=Todo.objects.filter(user=request.user,
    completed=True)
    return render(request,'./todo/completed.html',
    {'todos':todos})   

@login_required
def createtodo(request):
    form=TodoForm()
    message=''
    try:
        if request.method=='POST':
            print(request.POST)
            if request.user.is_authenticated:
                form=TodoForm(request.POST)
                todo=form.save(commit=False)
                todo.user=request.user
                todo.date_complated=datetime.now() if todo.completed else None
                todo.save()

                return redirect('todo')
    except Exception as e:
        print(e)
        message='資料輸入錯誤'

    return render(request,'./todo/createtodo.html',{'form':form,'message':message})
    

# Create your views here.
def todo(request):
    todos=None
    if request.user.is_authenticated:
        todos=Todo.objects.filter(user=request.user)
    print(todos)
    return render(request,'./todo/todo.html',{'todos':todos})

@login_required
def viewtodo(request,id):
    try:       
        todo=Todo.objects.get(id=id)
        if request.method=='GET':
            form=TodoForm(instance=todo)

        elif request.method=='POST':
            print(request.POST)
            if request.POST.get('update'):
                form=TodoForm(request.POST,instance=todo)
                if form.is_valid():
                    todo=form.save(commit=False)
                    todo.date_complated=datetime.now() if todo.completed else None
                    # 更新資料            
                    form.save()
            elif request.POST.get('delete'):
                todo.delete()
                return redirect('todo') 

        return render(request,'./todo/viewtodo.html',{'todo':todo,'form':form})
    except Exception as e:
        print(e)      
         
    return render(request,'./todo/404.html')