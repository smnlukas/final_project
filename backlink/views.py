from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse, get_object_or_404, reverse
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views import generic
from .forms import PostForm
from .models import Post

def index(request):

    return render(request, 'index.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request, f'Toks el.paštas jau užimtas!')
                return redirect('register')
            else:
                User.objects.create_user(username=username, email=email,
                                         password=password)
                return redirect('index')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

class PostListView(generic.ListView):
    template_name = 'mano-straipsniai.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_on')

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

from django.contrib import messages

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            if request.user.available_articles > 0:
                post = form.save(commit=False)
                post.save()
                request.user.available_articles -= 1
                request.user.save()
                return redirect('index')
            else:
                messages.error(request, 'You have no available articles.')
    else:
        form = PostForm(user=request.user)

    return render(request, 'rasyti-straipsni.html', {'form': form})