from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('albums/', views.get_albums, name='get_albums'),
]
    # path('userlist/', views.users_list, name='users_list'),
