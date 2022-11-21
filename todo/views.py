# under by Andy import
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Todo
from .forms import TodoForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
import random


@login_required
def genpassword(request):
    print(request.method)
    if request.method == 'POST':
        # a~z
        chars = [chr(c) for c in range(97, 123)]
        # None ==>False
        if request.POST.get('uppercase'):
            chars += [chr(c).upper() for c in range(97, 123)]

        if request.POST.get('numbers'):
            chars += list('0123456789')

        if request.POST.get('special'):
            chars += list('@#$%^&*')

        print(chars)
        # 取得輸入的長度
        length = eval(request.POST.get('length')) if request.POST.get('input-length') == '' \
            else eval(request.POST.get('input-length'))

        # 樣本數(不會重複，但不能取樣超過容器大小)
        # print(random.sample(chars,length))
        password = ''.join([random.choice(chars) for i in range(length)])

        # 變成字串?
        print(password)
        print(length)

        # return render(request, './todo/genpassword.html', {'password': password})
        return render(request, './todo/pwindex.html', {'password': '您的密碼為 : '+password})
    else:
        return redirect('pwindex')


@login_required
def pwindex(request):
    password = ''
    return render(request, './todo/pwindex.html', {'password': password})


@login_required
def sogi(request):
    return render(request, './todo/sogi.html')


@login_required
def bmi(request):
    return render(request, './todo/bmi.html')


@login_required
def fitness(request):
    return render(request, './todo/fitness.html')


@login_required
def completed_by_id(request, id):
    todo = Todo.objects.get(id=id)
    todo.completed = not todo.completed
    todo.date_complated = datetime.now() if todo.completed else None
    todo.save()
    return redirect('todo')


@login_required
def delete(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('todo')


@login_required
def completed(request):
    # 篩選已完成項目
    todos = Todo.objects.filter(user=request.user,
                                completed=True)
    return render(request, './todo/completed.html',
                  {'todos': todos})


@login_required
def createtodo(request):
    form = TodoForm()
    message = ''
    try:
        if request.method == 'POST':
            print(request.POST, request.FILES)
            if request.user.is_authenticated:
                form = TodoForm(request.POST, request.FILES)
                todo = form.save(commit=False)
                todo.user = request.user
                todo.date_complated = datetime.now() if todo.completed else None
                todo.save()

                return redirect('todo')
    except Exception as e:
        print(e)
        message = '資料輸入錯誤'

    return render(request, './todo/createtodo.html', {'form': form, 'message': message})


@login_required
def sorttodo(request):
    try:
        todos = Todo.objects.filter(user=request.user, completed=False)
        sort = request.COOKIES.get('sort')
        print(sort)
        sort = '1' if not sort or sort == '0' else '0'

        if sort == '1':
            todos = todos.order_by('-created')

    except Exception as e:
        print(e)

    response = render(request, './todo/todo.html', {'todos': todos})
    response.set_cookie('sort', sort)

    return response

# Create your views here.


def todo(request):
    todos = None
    if request.user.is_authenticated:
        # todos = Todo.objects.filter(user=request.user)
        todos = Todo.objects.filter(user=request.user, completed=False)
    print(todos)
    return render(request, './todo/todo.html', {'todos': todos})


@login_required
def viewtodo(request, id):
    try:
        todo = Todo.objects.get(id=id)
        if request.method == 'GET':
            form = TodoForm(instance=todo)

        elif request.method == 'POST':
            print(request.POST, request.FILES)
            if request.POST.get('update'):
                form = TodoForm(request.POST, request.FILES, instance=todo)
                if form.is_valid():
                    todo = form.save(commit=False)
                    todo.date_complated = datetime.now() if todo.completed else None
                    # 更新資料
                    form.save()
            elif request.POST.get('delete'):
                todo.delete()
                return redirect('todo')

        return render(request, './todo/viewtodo.html', {'todo': todo, 'form': form})
    except Exception as e:
        print(e)

    return render(request, './todo/404.html')
