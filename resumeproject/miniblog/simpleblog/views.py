from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.

def home(request):
    posts= Post.objects.all()
    return render(request, 'simpleblog/home.html', {'posts': posts})


def about(request):
    return render(request, 'simpleblog/about.html')


def contact(request):
    return render(request, 'simpleblog/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts= Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'simpleblog/dashboard.html',{'posts': posts, 'fname': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request, request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user=user)
                    messages.success(request, "You are currently logged in !!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'simpleblog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')



def user_signup(request):
    if request.method == 'POST':
        form= SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You are succcessfully registered')
            user = form.save()
            group = Group.objects.get(name= 'Author')
            user.groups.add(group)


    else:
        form = SignUpForm()
    return render(request, 'simpleblog/signup.html',{'form': form})


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst= Post(title= title, desc= desc)
                pst.save()
                form= PostForm()
        else:
            form= PostForm()
        return render(request, 'simpleblog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi= Post.objects.get(id=id)
            form = PostForm(request.POST, instance= pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(id = id)
            form = PostForm(instance=pi)
        return render(request, 'simpleblog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi= Post.objects.get(id= id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')