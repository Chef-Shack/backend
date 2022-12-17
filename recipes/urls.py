from django.urls import path
from . import views

urlpatterns = [
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('get_recipe', views.get_recipe, name='get_recipe'),
    path('update_recipe', views.update_recipe, name='update_recipe'),
    path('delete_recipe', views.delete_recipe, name='delete_recipe'),
    path('authors_recipes', views.authors_recipes, name='authors_recipes'),
    path('category_recipes', views.category_recipes, name='category_recipes'),
    path('get_all_recipes', views.get_all_recipes, name='get_all_recipes'),
]
