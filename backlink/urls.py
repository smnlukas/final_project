from django.urls import path, include
from . import views
from .views import create_post, profile_update, article_order, order_success


urlpatterns = [
    path('',  views.index, name='index'),
    path('registeracija/', views.register, name='register'),
    path('mano-straipsniai/',  views.PostListView.as_view(), name='my_articles'),
    path('rasyti-straipsni/', create_post, name='create_post'),
    path('mano-paskyra/', profile_update, name='my_profile'),
    path('uzsakymas/', views.article_order, name='article_order'),
    path('uzsakymas-atliktas/', order_success, name='order_success'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]