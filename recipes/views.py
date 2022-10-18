from django.http import HttpResponse, JsonResponse
from recipes.models import Recipe

# Create your views here.
def create_recipe(request):
    if request.user.is_authenticated and request.user.username != 'AnonymousUser':
        if request.method == 'POST':
            recipe_title = request.POST['recipe_title']
            recipe_description = request.POST['recipe_description']
            author = request.user
            recipe = Recipe(recipe_title=recipe_title, recipe_description=recipe_description, author=author)
            recipe.save()

            return JsonResponse({'recipe': recipe})
    return HttpResponse(status=404)