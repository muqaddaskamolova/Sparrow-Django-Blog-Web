from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from blog.forms import *
from blog.models import Post, Category, Developer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
def index(request):
    posts = Post.objects.all()
    posts = posts.order_by('-created_at')
    categories = Category.objects.all()
    context = {
        'title': 'SPARROW - Home',
        'posts': posts,
        'categories': categories,

    }
    return render(request, 'blog/index.html', context)


# class HomeView(ListView):
# model = Post
# template_name = 'blog/index.html'
def category_page(request, category_id):
    posts = Post.objects.filter(category_id=category_id)
    posts = posts.order_by('-created_at')

    category = Category.objects.get(pk=category_id)
    categories = Category.objects.all()
    context = {
        'title': f"Category: {category.title}",
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'blog/index.html', context)


def about_dev(request):
    developers = Developer.objects.all()

    context = {
        'title': 'About Developers',
        'developers': developers
    }
    return render(request, 'blog/about_dev.html', context)


def search_results(request):
    word = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=word) | Q(content__icontains=word)
                                )
    context = {
        'posts': posts.order_by('-created_at')
    }
    return render(request, 'blog/index.html', context)


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect('index')
        else:
            pass
    else:
        form = PostForm()

        context = {
            'title': 'New Post',
            'form': form,
        }
        return render(request, 'blog/post_form.html', context)


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = Post.objects.create(**form.cleaned_data)
            project.save()
            return redirect('index')
        else:
            pass
    else:
        form = ProjectForm()

        context = {
            'title': 'New Project',
            'form': form,
        }
        return render(request, 'blog/project_form.html', context)


def header(request):
    context = {}

    return render(request, 'components/_header.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect('index')
            else:
                messages.error(request, 'You have not logged in,  Or  your login or password is wrong!')
                return redirect('login')
        else:
            messages.error(request, 'You have not logged in,  Or  your login or password is wrong!')
            return redirect('login')
    else:
        form = LoginForm()
        context = {
            'title': 'LOGIN',
            'form': form
        }
        return render(request, 'blog/user_login.html', context)


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.warning(request, 'You have successfully logged out!')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered! Sign in!')
            return redirect('login')
        for field in form.errors:
            messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

        context = {
            'title': 'REGISTER',
            'form': form
        }
        return render(request, 'blog/register.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.views += 1
    post.save()

    context = {
        'title': post.title,
        'post': post

    }
    if request.user.is_authenticated:
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=post)
    user = request.user
    if user.is_authenticated:
        mark, created = Like.objects.get_or_create(user=user, post=post)
        if created:
            context['like'] = False
            context['dislike'] = False
        else:
            context['like'] = mark.like
            context['dislike'] = mark.dislike

    else:
        context['like'] = False
        context['dislike'] = False

    marks = Like.objects.filter(post=post)
    likes_count = len([i for i in marks if i.like])
    dislikes_count = len([i for i in marks if i.dislike])
    context['likes_count'] = likes_count
    context['dislikes_count'] = dislikes_count
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='login')
def update_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', id)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text)
                return redirect('update', id)
    else:
        form = PostForm(instance=post)

        context = {
            'title': 'UPDATE POST',
            'form': form,
        }

        return render(request, 'blog/post_form.html', context)


@login_required(login_url='login')
def delete_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    context = {
        'post': post
    }

    return render(request, 'blog/confirm_delete.html', context)


def save_comment(request, pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = Post.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Your comment is added!')
        return redirect('post', pk)


@login_required(login_url='login')
def add_or_delete_mark(request, post_id, action):
    user = request.user
    if user.is_authenticated:
        post = Post.objects.get(pk=post_id)
        mark, created = Like.objects.get_or_create(user=user, post=post)
        if action == 'add_like':
            mark.like = True
            mark.dislike = False
        elif action == 'add_dislike':
            mark.like = False
            mark.dislike = True
        elif action == 'delete_like':
            mark.like = False
        elif action == 'delete_dislike':
            mark.dislike = False

            mark.save()
            return redirect('post', post.pk)

    else:
        return redirect('login')


@login_required(login_url='login')
def user_profile(request):
    context = {}

    return render(request, 'blog/user_profile.html', context)


def contact_us(request, ):
    if request.method == 'POST':
        message_name = request.POST['message-name'],
        message_email = request.POST['message-email'],
        subject_name = request.POST['subject-name'],
        message = request.POST['message'],

        send_mail(
            message_name,
            subject_name,
            message,
            message_email,
            ['kamolovamuqaddas@gmail.com']
        )


def map_page(request):
    context = {}

    return render(request, 'blog/map_page.html', context)
