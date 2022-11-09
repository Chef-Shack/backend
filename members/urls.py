from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('register_admin', views.register_admin, name='register_admin'),
    path('get_user_by_id/<int:id>', views.get_user_by_id, name='get_user_by_id'),
    path('get_user_by_name/<str:username>', views.get_user_by_name, name='get_user_by_name'),
    path('like_recipe', views.like_recipe, name='like_recipe'),
    path('unlike_recipe', views.unlike_recipe, name='unlike_recipe')
]
