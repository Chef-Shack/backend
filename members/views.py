from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from members.models import UserProperties



# Create your views here.

@ensure_csrf_cookie
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'user': username, 'password': password, 'success': True})
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
        userProperties = UserProperties.objects.create(user=user, isPremium=False)
        return JsonResponse({'user': username, 'email': email, 'isPremium': userProperties.isPremium, 'success': True})
    else:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def get_user_by_id(request):
    if request.method == 'POST':
        id = request.POST['id']
        user = User.objects.get(pk=id)
        if user.is_superuser:
            return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': True, 'success': True})
        userProperties = UserProperties.objects.get(pk=user)
        return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': userProperties.isPremium,
                             'success': True})
    return JsonResponse({'success': False})


@ensure_csrf_cookie
def get_user_by_name(request, username):
    user = User.objects.all().filter(username=username).first()
    if user.is_superuser:
        return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': True, 'success': True})
    userProperties = UserProperties.objects.get(pk=user)
    try:
        return JsonResponse({'username': user.username, 'email': user.email, 'isPremium': userProperties.isPremium,
                             'success': True})
    except Exception:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def get_user_instance(request):
        try:
            if request.user.is_superuser:
                return JsonResponse({'username': request.user.username, 'email': request.user.email, 'isPremium': True})
            userProperties = UserProperties.objects.get(pk=request.user)
            return JsonResponse({'username': request.user.username, 'email': request.user.email, 'isPremium': userProperties.isPremium})
        except Exception:
            return JsonResponse({'username': request.user.username, 'isAuthenticated': request.user.is_authenticated})


