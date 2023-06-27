from django.urls import path, include
from . import views



urlpatterns = [
    path('',  views.index, name='index'),
    path('registeracija/', views.register, name='register'),
    path('mano-straipsniai/',  views.PostListView.as_view(), name='my_articles'),
    path('rasyti-straipsni/', views.create_post, name='create_post'),
    path('mano-paskyra/', views.profile_update, name='my_profile'),
    path('uzsakymas/', views.article_order, name='article_order'),
    path('uzsakymas-atliktas/', views.order_success, name='order_success'),
    path('mano-uzsakymai/', views.OrdersListView.as_view(), name='my_orders'),
    path('straipsnis/<int:pk>/', views.PostDetailView.as_view(), name='post_details'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]