from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('get_user_by_id', views.get_user_by_id, name='get_user_by_id'),
    path('get_user_by_name/<str:username>', views.get_user_by_name, name='get_user_by_name'),
    path('get_user_instance', views.get_user_instance, name='get_user_instance')
]
