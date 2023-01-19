from django.http import HttpResponse, JsonResponse
from recipes.models import Recipe
from django.contrib.auth.models import User


# Create your views here.
# CRUD Create Read Update Write
def create_recipe(request):
    if request.method == 'POST':
        # Fields
        recipe_title = request.POST.get('recipe_title')
        recipe_description = request.POST.get('recipe_description')
        author = request.POST.get('author')
        image = request.POST.get('image')
        ingredients = request.POST.get('ingredients')
        procedure = request.POST.get('procedure')
        category = request.POST.get('category')

        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            return JsonResponse({'success': False})

        recipe = Recipe(recipe_title=recipe_title, recipe_description=recipe_description, author=author, image=image,
                        ingredients=ingredients.split(','), procedure=procedure.split(','), category=category, likes=0)
        recipe.save()

        return JsonResponse({
            'id': recipe.id,
            'authorID': recipe.author,
            'pub_date': recipe.pub_date,
            'recipe_title': recipe.recipe_title,
            'recipe_description': recipe.recipe_description,
            'image': recipe.image,
            'ingredients': recipe.ingredients,
            'procedure': recipe.procedure,
            'likes': recipe.likes,
            'success': True
        })
    return JsonResponse({'success': False})


def get_recipe(request):
    if request.method == 'POST':
        id = request.POST['id']
        r = Recipe.objects.get(pk=id)
        authorUsername = User.objects.get(pk=r.author).username
        return JsonResponse({
            'id': r.id,
            'author': r.author,
            'username': authorUsername,
            'pub_date': r.pub_date,
            'recipe_title': r.recipe_title,
            'recipe_description': r.recipe_description,
            'image': r.image,
            'ingredients': r.ingredients,
            'procedure': r.procedure,
            'category': r.category,
            'likes': r.likes,
            'success': True
        })
    return JsonResponse({'success': False})


def update_recipe(request):
    if request.method == 'POST':
        author = request.POST['username']
        r = Recipe.objects.get(author=author)

        for k in request.POST:
            v = request.POST[k]
            if v == '':
                continue
            exec(f'r.{k} = "{v}"')

        r.save()
        return JsonResponse({
            'id': r.id,
            'author': r.author,
            'pub_date': r.pub_date,
            'recipe_title': r.recipe_title,
            'recipe_description': r.recipe_description,
            'image': r.image,
            'ingredients': r.ingredients,
            'procedure': r.procedure,
            'category': r.category,
            'likes': r.likes,
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
        username = request.POST['username']
        r = Recipe.objects.all().filter(author=username)
        list_of_recipes = []
        for recipe in r:
            temp_dict = {
                'id': recipe.id,
                'author': recipe.author,
                'pub_date': recipe.pub_date,
                'recipe_title': recipe.recipe_title,
                'recipe_description': recipe.recipe_description,
                'image': r.image,
                'ingredients': r.ingredients,
                'procedure': r.procedure,
                'category': r.category,
                'likes': r.likes,
                'success': True
            }
            list_of_recipes.append(temp_dict)
        return JsonResponse(list_of_recipes, safe=False)
    return JsonResponse({'success': False})


def category_recipes(request):
    if request.method == 'POST':
        category = request.POST['category']
        r = Recipe.objects.all().filter(category=category)
        list_of_categories = []
        for recipe in r:
            temp_dict = {
                'id': recipe.id,
                'author': recipe.author,
                'pub_date': recipe.pub_date,
                'recipe_title': recipe.recipe_title,
                'recipe_description': recipe.recipe_description,
                'image': r.image,
                'ingredients': r.ingredients,
                'procedure': r.procedure,
                'category': r.category,
                'likes': r.likes,
                'success': True
            }
            list_of_categories.append(temp_dict)
        return JsonResponse(list_of_categories, safe=False)
    else:
        return JsonResponse({'success': False})


def get_all_recipes(request):
    global data
    recipes = []
    for r in Recipe.objects.all():
        authorUsername = User.objects.get(pk=r.author).username
        recipes.append({
            'id': r.id,
            'author': r.author,
            'username': authorUsername,
            'pub_date': r.pub_date,
            'recipe_title': r.recipe_title,
            'recipe_description': r.recipe_description,
            'image': r.image,
            'ingredients': r.ingredients,
            'procedure': r.procedure,
            'category': r.category,
            'likes': r.likes
        })
    return JsonResponse({'recipes': recipes, 'success': True})
