from django.urls import path, include
from . import views
from .views import create_post


urlpatterns = [
    path('',  views.index, name='index'),
    path('register/', views.register, name='register'),
    path('mano-straipsniai/',  views.PostListView.as_view(), name='my_articles'),
    path('rasyti-straipsni/', create_post, name='create_post'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]