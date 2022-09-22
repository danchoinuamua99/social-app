from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Profile, Post

from social.forms import SignUpForm
# Create your views here.


@login_required(login_url='signin')
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()[:2]
    return render(
        request,
        'index.html',
        context={
            'user_profile': user_profile,
            'posts': posts
        }
    )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # log user in and redirect to settings page
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            # create a Profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('index')
        else:
            return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password not correct! ')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        user_profile.bio = request.POST.get('bio')
        user_profile.location = request.POST.get('location')
        if request.FILES.get('image') is not None:
            user_profile.profileimg = request.FILES.get('image')

        user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', context={'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):
    user = request.user.username
    image = request.FILES.get('image_upload')
    print(image)
    caption = request.POST['caption']
    Post.objects.create(user=user, image=image, caption=caption)
    posts = Post.objects.order_by('-created_at')[:2]

    return render(request, 'partials/post-list.html', {'posts': posts})


class PostList(LoginRequiredMixin, ListView):
    template_name = 'partials/post-list.html'
    model = Post
    paginate_by = 1
    context_object_name = 'posts'

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')[2:]
