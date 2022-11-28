from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from members.models import UserProperties
from recipes.models import Recipe


# Create your views here.

@ensure_csrf_cookie
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'id': request.user.id, 'user': username, 'password': password, 'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def logout_user(request):
    logout(request)
    return JsonResponse({'success': True})


@ensure_csrf_cookie
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        userProperties = UserProperties.objects.create(user=user, isPremium=False, likedRecipes=[])
        return JsonResponse({'user': username, 'email': email, 'isPremium': userProperties.isPremium,
                             'likedRecipes': userProperties.likedRecipes, 'success': True})
    else:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def register_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_superuser(username=username, password=password, email=email)
        userProperties = UserProperties.objects.create(user=user, isPremium=True, likedRecipes=[])
        return JsonResponse({'user': username, 'email': email, 'isPremium': userProperties.isPremium,
                             'likedRecipes': userProperties.likedRecipes, 'success': True})
    else:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def get_user_by_id(request, id):
    try:
        user = User.objects.get(pk=id)
        userProperties = UserProperties.objects.get(pk=user)
        return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': userProperties.isPremium,
                             'likedRecipes': userProperties.likedRecipes, 'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def get_user_by_name(request, username):
    user = User.objects.all().filter(username=username).first()
    try:
        userProperties = UserProperties.objects.get(pk=user)
        return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': userProperties.isPremium,
                             'likedRecipes': userProperties.likedRecipes, 'success': True})
    except AttributeError:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def like_recipe(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        recipeID = request.POST.get('recipeID')

        recipe = Recipe.objects.get(pk=recipeID)
        user = User.objects.get(username=username)
        userProperties = UserProperties.objects.get(user=user)

        if recipe.id in userProperties.likedRecipes:
            return JsonResponse({'success': False})
        else:
            recipe.likes += 1
            recipe.save()
            userProperties.likedRecipes.append(recipe.id)
            userProperties.save()
            return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': userProperties.isPremium,
                    'likedRecipes': userProperties.likedRecipes, 'success': True})


@ensure_csrf_cookie
def unlike_recipe(request):
    if request.method == 'POST':
        username = request.POST['username']
        recipeID = request.POST['recipeID']

        recipe = Recipe.objects.get(pk=recipeID)
        user = User.objects.get(username=username)
        userProperties = UserProperties.objects.get(user=user)

        if recipe.id in userProperties.likedRecipes:
            recipe.likes -= 1
            recipe.save()
            userProperties.likedRecipes.remove(recipe.id)
            userProperties.save()
            return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': userProperties.isPremium,
                                 'likedRecipes': userProperties.likedRecipes, 'success': True})
        else:
            return JsonResponse({'success': False})
