from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views import generic
from .forms import PostForm, UserProfileUpdateForm, ArticleOrderForm
from .models import Post, User

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
                return redirect('login')
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


@login_required
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
    else:
        form = UserProfileUpdateForm(instance=user)

    profile_data = {
        'available_articles': user.available_articles,
    }

    return render(request, 'mano-paskyra.html', {'form': form, 'profile_data': profile_data})

def create_article_order(request):
    if request.method == 'POST':
        form = ArticleOrderForm(request.POST)
        if form.is_valid():
            article_order = form.save(commit=False)
            article_order.user = request.user
            article_order.save()
            return redirect('order_success')
    else:
        form = ArticleOrderForm()

    return render(request, 'uzsakymas.html', {'form': form})

def order_success(request):
    return render(request, 'uzsakymas-atliktas.html')