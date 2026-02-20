from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Todo
from django.contrib.auth.models import User
# from django.contrib.auth import logout


# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid credentials'})

#     return render(request, 'login.html')



def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         User.objects.create_user(username=username, password=password)
#         return redirect('login')

#     return render(request, 'signup.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'signup.html')




# @login_required
# def home(request):
#     todos = Todo.objects.filter(user=request.user)
#     return render(request, 'home.html', {'todos': todos})

@login_required
def home(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'home.html', {'todos': todos})


@login_required
def create_todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            Todo.objects.create(
                title=title,
                description=description,
                user=request.user
            )

    return redirect('home')



@login_required
def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if request.method == "POST":
        todo.completed = request.POST.get('completed') == 'on'
        todo.save()

    return redirect('home')



@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('home')



def user_logout(request):
    logout(request)
    return redirect('login')