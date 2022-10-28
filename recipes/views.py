from django.http import HttpResponse, JsonResponse
from recipes.models import Recipe


# Create your views here.
# CRUD Create Read Update Write
def create_recipe(request):
    if request.user.is_authenticated and request.user.username != 'AnonymousUser':
        if request.method == 'POST':
            recipe_title = request.POST['recipe_title']
            recipe_description = request.POST['recipe_description']
            author = request.user
            recipe = Recipe(recipe_title=recipe_title, recipe_description=recipe_description, author=author)
            recipe.save()

            return JsonResponse({
                'id': recipe.id,
                'authorID': recipe.author.id,
                'pub_date': recipe.pub_date,
                'recipe_title': recipe.recipe_title,
                'recipe_description': recipe.recipe_description,
                'success': True
            })
    return JsonResponse({'success': False})


def get_recipe(request):
    if request.method == 'POST':
        id = request.POST['id']
        r = Recipe.objects.get(pk=id)
        return JsonResponse({
            'id': r.id,
            'authorID': r.author.id,
            'pub_date': r.pub_date,
            'recipe_title': r.recipe_title,
            'recipe_description': r.recipe_description,
            'success': True
        })
    return JsonResponse({'success': False})

def update_recipe(request):
    if request.method == 'POST':
        id = request.POST['id']
        r = Recipe.objects.get(pk=id)

        for k in request.POST:
            v = request.POST[k]
            if v == '':
                continue
            exec(f'r.{k} = "{v}"')

        r.save()
        return JsonResponse({
            'id': r.id,
            'authorID': r.author.id,
            'pub_date': r.pub_date,
            'recipe_title': r.recipe_title,
            'recipe_description': r.recipe_description,
            'success': True
        })

    return JsonResponse({'success': False})


def delete_recipe(request):
    if request.method == 'POST':
        id = request.POST['id']
        r = Recipe.objects.get(pk=id)
        if r.author_id == request.user.id or request.user.is_superuser:
            r.delete()
        else:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def authors_recipes(request):
    if request.method == 'POST':
        id = request.POST['id']
        r = Recipe.objects.all().filter(author_id=id)
        list_of_recipes = []
        for recipe in r:
            temp_dict = {
                'id': recipe.id,
                'authorID': recipe.author.id,
                'pub_date': recipe.pub_date,
                'recipe_title': recipe.recipe_title,
                'recipe_description': recipe.recipe_description,
                'success': True
            }
            list_of_recipes.append(temp_dict)
        return JsonResponse(list_of_recipes, safe=False)
    return JsonResponse({'success': False})
