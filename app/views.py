"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.http import HttpResponse
from .forms import FeedbackForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария
from .forms import BlogForm


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
              'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
           'title':'Контакты',
           'message':'Страница с нашими контактами.',
           'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )
def links(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
         request, 
        'app/links.html',
       {'title':'Полезные ресурсы',
        'year':datetime.now().year, 
       }
    )
def feedback(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Если форма валидна, обработка данных отзыва
            return render(request, 'app/success.html', {'form': form})
    else:
        form = FeedbackForm() 
    return render(request, 'app/feedback.html', {'form': form})
def success_view(request):
    """Render a success page."""
    return render(request, 'app/success.html')

def registration(request): 
    """Renders the registration page.""" 
    if request.method == "POST":         # после отправки формы
        regform = UserCreationForm(request.POST) 
        if regform.is_valid():           # валидация полей формы
            reg_f = regform.save(commit=False)  # не сохраняем автоматически данные формы
            reg_f.is_staff = False      # запрещен вход в административный раздел
            reg_f.is_active = True       # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления полей
            return redirect("home") # переадресация на главную страницу после регистрации
    else: 
        regform = UserCreationForm() # создание объекта формы для ввода данных
    assert isinstance(request, HttpRequest)
    return render(
        request, 
        'app/registration.html',
        {
            'regform': regform,     # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )
def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
         'title':'Блог',
         'posts': posts, # передача списка статей в шаблон веб-страницы
         'year':datetime.now().year,
         }
        )
def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest) 
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру 
    comments = Comment.objects.filter(post=parametr).order_by('-date')  # Сортировка комментариев по убыванию даты
    if request.method == "POST":  # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user  # добавляем автора комментария
            comment_f.date = datetime.now()  # добавляем текущую дату
            comment_f.post = Blog.objects.get(id=parametr)  # добавляем статью, для которой данный комментарий
            comment_f.save()  # сохраняем комментарий
            return redirect('blogpost', parametr=post_1.id)  # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm()  # создание формы для ввода комментария
    return render(
              request,
              'app/blogpost.html',
              {
                  'post_1': post_1,  # передача конкретной статьи в шаблон веб-страницы
                  'comments': comments,  # передача комментариев в шаблон веб-страницы
                  'form': form,  # передача формы в шаблон веб-страницы
                  'year': datetime.now().year,
                  }
              )

def newpost(request): 
    """Renders the new post page."""
    assert isinstance(request, HttpRequest)
    blogform = BlogForm()   # инициализация переменной blogform

    if request.method == "POST":    # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            if request.user.is_authenticated:  # Проверяем, аутентифицирован ли пользователь
                blog_f.author = request.user    # Используем аутентифицированного пользователя в качестве автора
            else:
                # Обработка случая, когда пользователь не аутентифицирован
                # Например, можно перенаправить его на страницу входа
                return redirect('login')
            blog_f.posted = datetime.now()
            blog_f.save()           # сохраняем изменения после добавления полей
            return redirect('blog') # переадресация на страницу Блог после создания статьи Блога
            
    return render(
        request,
        'app/newpost.html',
        { 
            'blogform': blogform, # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year':datetime.now().year,
        }
    )
def videopost(request):
    """Renders the video post page."""
    assert isinstance(request, HttpRequest)
    # Добавьте код здесь для обработки запроса и рендеринга страницы videopost
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видеостатья',
            'message': 'Это видеостатья.',
            'year': datetime.now().year,
        }
    )
