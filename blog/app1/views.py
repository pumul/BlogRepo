from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group


def home_view(request):
    data = Post.objects.all()
    context = {
        'post_data': data
    }
    return render(request, "app1/home.html", context)


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':

            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data["username"]
                upass = form.cleaned_data["password"]
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/profile/')
            context = {
                'form': form,
            }
            return render(request, "app1/login.html", context)

        else:
            form = LoginForm()
            context = {
                'form': form,
            }
            return render(request, "app1/login.html", context)
    else:
        return HttpResponseRedirect('/profile/')


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':

            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Congratulation!! you become an author.')
                return HttpResponseRedirect('/login/')
            context = {
                'form': form,
            }
            return render(request, "app1/signup.html", context)

        else:
            form = SignupForm()
            context = {
                'form': form,
            }
            return render(request, "app1/signup.html", context)
    else:
        return HttpResponseRedirect('/profile/')


def profile_view(request):
    if request.user.is_authenticated:
        context = {

        }
        return render(request, "app1/profile.html", context)
    messages.info(request, 'You have to login here first.')
    return HttpResponseRedirect('/login/')


def dashboard_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST["title"]
            desc = request.POST["desc"]
            image_url = request.POST["image_url"]
            Post(title=title, desc=desc, image_url=image_url, author=request.user).save()
            messages.success(request, 'Your blog posted.')
            data = Post.objects.filter(author=request.user)
            context = {
                'post_data': data
            }
            return render(request, "app1/dashboard.html", context)
        else:
            data = Post.objects.filter(author=request.user)
            context = {
                'post_data': data
            }
            return render(request, "app1/dashboard.html", context)
    messages.info(request, 'You have to login here first.')
    return HttpResponseRedirect('/login/')


def update_post(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            old_data = Post.objects.get(id=pk)
            title = request.POST["title"]
            image_url = request.POST["image_url"]
            desc = request.POST["desc"]
            Post.objects.filter(id=pk).update(title=title,image_url=image_url,desc=desc,author=old_data.author)
            messages.success(request, 'Post updated successfully.')
            return HttpResponseRedirect('/dashboard/')
        else:
            data = Post.objects.get(id=pk)
            context = {
                    'post_data': data
                }
            return render(request, "app1/update_post.html", context)
    messages.info(request, 'You have to login here first.')
    return HttpResponseRedirect('/login/')


def delete_post(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Post.objects.get(id=pk).delete()
            messages.success(request, 'Post Deleted Successfully.')
            return HttpResponseRedirect('/dashboard/')
        else:
            data = Post.objects.get(id=pk)
            context = {
                    'post_data': data
                }
            return render(request, "app1/delete_post.html", context)
    messages.info(request, 'You have to login here first.')
    return HttpResponseRedirect('/login/')

def about_view(request):
    context = {

    }
    return render(request, "app1/about.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Successfully logged out!!')
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/')
