import json
from datetime import date

from django.conf import settings
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, ExpressionWrapper, IntegerField, QuerySet
from django.db import models
from django.db.models.functions import ExtractYear
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_http_methods, require_GET, require_POST
)
from django.forms.models import model_to_dict

from api.models import Hobby, CustomUser, FriendRequest
from api.forms import LoginForm, SignupForm


@require_GET
@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    """
    Redirects to the single-page application (SPA) base URL.
    """
    return render(request, 'api/spa/index.html', {})


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    """
    View to log in the user.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data['email']
            password: str = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm
    return render(request, 'login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def signup_view(request: HttpRequest) -> HttpResponse:
    """
    View to sign up a new user.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the new user
            user: CustomUser = form.save()

            # Authenticate using the email and password
            email: str = form.cleaned_data.get('email')
            password: str = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, username=email, password=password)

            if authenticated_user:
                login(request, authenticated_user)
                return redirect('/')  # Replace '/' with your desired success URL
            else:
                form.add_error(None, "Account created, but there was an issue logging you in. Please log in manually.")
        else:
            form.add_error(None, "There was an error creating your account. Please check the form and try again.")
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


@require_GET
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    View to log out the user.
    """
    logout(request)
    return redirect('login')


@require_GET
@login_required
def get_hobbies(request: HttpRequest) -> HttpResponse:
    """
    View to get all hobbies.
    """
    hobbies: list[dict[str, str]] = list(Hobby.objects.values('name', 'description'))
    return JsonResponse({'hobbies': hobbies})


@require_GET
@login_required
def get_users(request: HttpRequest) -> HttpResponse:
    """
    View to get all users.
    """
    users: QuerySet[CustomUser, CustomUser] = CustomUser.objects.prefetch_related('hobbies')
    user_data: list[dict[str, object]] = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'hobbies': [hobby.name for hobby in user.hobbies.all()]
        }
        for user in users
    ]
    return JsonResponse({'users': user_data})


@require_GET
@login_required
def get_user(request: HttpRequest, user_id: int = None) -> HttpResponse:
    """
    View to get a user's details. If no user_id is provided, return the currently logged-in user's details.
    """
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(CustomUser.objects.prefetch_related('hobbies', 'friends'), id=user_id)

    user_data: dict[str, any] = model_to_dict(user, fields=['id', 'username', 'first_name', 'last_name', 'email', 'date_of_birth'])

    user_data['hobbies']: list[dict[str, any]] = [
        {'id': hobby.id, 'name': hobby.name} for hobby in user.hobbies.all()
    ]

    user_data['friends']: list[dict[str, any]] = [
        {'id': friend.id, 'username': friend.username}
        for friend in user.friends.all()
    ]

    sent_requests: list[FriendRequest] = user.sent_friend_requests.select_related('receiver').all()
    received_requests: list[FriendRequest] = user.received_friend_requests.select_related('sender').all()

    user_data['sent_requests']: list[dict[str, any]] = [
        {
            'id': friend_request.id,
            'receiver_id': friend_request.receiver.id,
            'receiver_username': friend_request.receiver.username,
            'status': friend_request.status
        }
        for friend_request in sent_requests
    ]
    user_data['received_requests']: list[dict[str, any]] = [
        {
            'id': friend_request.id,
            'sender_id': friend_request.sender.id,
            'sender_username': friend_request.sender.username,
            'status': friend_request.status
        }
        for friend_request in received_requests
    ]

    return JsonResponse({'user': user_data})


@require_http_methods(['PUT', 'PATCH'])
@login_required
def update_user(request: HttpRequest) -> HttpResponse:
    """
    View to delete a hobby.
    """
    user = request.user

    try:
        data: dict[str, any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if request.method == "PUT":
        required_fields = ['email', 'username', 'first_name', 'last_name', 'date_of_birth']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return JsonResponse(
                {'error': f'Missing required fields: {", ".join(missing_fields)}'},
                status=400
            )

        user.email = data['email']
        user.username = data['username']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.date_of_birth = data['date_of_birth']

        if 'password' in data:
            user.set_password(data['password'])
            
    elif request.method == "PATCH":
        for field in ['email', 'username', 'first_name', 'last_name', 'password', 'date_of_birth']:
            if field in data:
                if field == 'password':
                    user.set_password(data['password'])
                else:
                    setattr(user, field, data[field])
    user.save()

    if 'password' in data:
        update_session_auth_hash(request, user)

    return JsonResponse({
        'message': 'User information updated successfully.',
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'hobbies': list(user.hobbies.values('id', 'name')),
        }
    }, status=200)


@require_GET
@login_required
def get_similar_users(request: HttpRequest) -> HttpResponse:
    """
    View to get users in descending order based on similarities and filtered by age range.
    """
    user = request.user

    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')

    current_year: int = date.today().year

    users_with_age: QuerySet = CustomUser.objects.annotate(
        age=ExpressionWrapper(
            current_year - ExtractYear(F('date_of_birth')),
            output_field=IntegerField()
        )
    )

    filtered_users: QuerySet = users_with_age.exclude(id=user.id)
    if min_age is not None:
        filtered_users = filtered_users.filter(age__gte=int(min_age))
    if max_age is not None:
        filtered_users = filtered_users.filter(age__lte=int(max_age))

    similar_users: QuerySet = (
        filtered_users
        .annotate(
            similarity=models.Count('hobbies', filter=models.Q(hobbies__in=user.hobbies.all()))
        )
        .prefetch_related('hobbies')
        .order_by('-similarity')
    )

    user_hobby_ids = user.hobbies.values_list('id', flat=True)

    similar_users_data: list[dict[str, any]] = [
        {
            'id': similar_user.id,
            'username': similar_user.username,
            'email': similar_user.email,
            'age': similar_user.age,
            'similarity': similar_user.similarity,
            'common_hobbies': [
                hobby.name
                for hobby in similar_user.hobbies.all()
                if hobby.id in user_hobby_ids
            ]
        }
        for similar_user in similar_users
    ]

    return JsonResponse({'user': {'id': user.id, 'username': user.username}, 'similar_users': similar_users_data})



@require_POST
@login_required
def send_friend_request(request: HttpRequest, receiver_id: int) -> HttpResponse:
    """
    View to send a friend request.
    """
    sender = request.user
    receiver: CustomUser = get_object_or_404(CustomUser, id=receiver_id)

    if sender == receiver:
        return JsonResponse({'error': 'You cannot send a friend request to yourself.'}, status=400)

    existing_request: FriendRequest = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
    if existing_request:
        return JsonResponse({'error': 'Friend request already sent.'}, status=400)

    reverse_request: FriendRequest = FriendRequest.objects.filter(sender=receiver, receiver=sender).first()
    if reverse_request:
        return JsonResponse({'error': 'The receiver has already sent you a friend request.'}, status=400)

    FriendRequest.objects.create(sender=sender, receiver=receiver)
    return JsonResponse({'message': 'Friend request sent successfully.'})


@require_POST
@login_required
def accept_friend_request(request: HttpRequest, request_id: int) -> HttpResponse:
    """
    View to accept a friend request.
    """
    friend_request: FriendRequest = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    if friend_request.status != 'pending':
        return JsonResponse({'error': 'Friend request is no longer pending.'}, status=400)

    friend_request.status = 'accepted'
    friend_request.save()

    # Add both users to each other's friends list
    friend_request.sender.friends.add(friend_request.receiver)
    friend_request.receiver.friends.add(friend_request.sender)

    return JsonResponse({'message': 'Friend request accepted.'})


@require_POST
@login_required
def decline_friend_request(request: HttpRequest, request_id: int) -> HttpResponse:
    """
    View to decline a friend request.
    """
    friend_request: FriendRequest = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    if friend_request.status != 'pending':
        return JsonResponse({'error': 'Friend request is no longer pending.'}, status=400)

    friend_request.status = 'declined'
    friend_request.save()

    return JsonResponse({'message': 'Friend request declined.'})


@require_POST
@login_required
def add_hobby(request: HttpRequest) -> HttpResponse:
    """
    View to add a hobby to the user's list of hobbies.
    """
    try:
        data: dict[str, any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    name: str = data.get('name', '')

    if not name:
        return JsonResponse({'error': 'Hobby name is required.'}, status=400)

    normalised_name: str = name.strip().lower()

    user = request.user

    hobby: Hobby
    created: bool
    hobby, created = Hobby.objects.get_or_create(
        name=normalised_name.capitalize(),
        defaults={'name': normalised_name.capitalize()}
    )

    user.hobbies.add(hobby)

    return JsonResponse({
        'message': 'Hobby added successfully.',
        'hobby_id': hobby.id,
        'hobby_name': hobby.name,
        'created': created
    }, status=201)


@require_http_methods(['PATCH'])
@login_required
def update_hobby(request: HttpRequest, hobby_id: int) -> HttpResponse:
    """
    View to delete a hobby.
    """
    try:
        data: dict[str, any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    name: str = data.get('name', '')

    if not name:
        return JsonResponse({'error': 'Hobby name is required.'}, status=400)

    hobby: Hobby = get_object_or_404(Hobby, id=hobby_id)
    if hobby.name != name:
        hobby.name = name
        hobby.save()

    return JsonResponse({'message': 'Hobby updated successfully.'}, status=200)


@require_http_methods(['DELETE'])
@login_required
def delete_hobby(request: HttpRequest, hobby_id: int) -> HttpResponse:
    """
    View to delete a hobby.
    """
    hobby: Hobby = get_object_or_404(Hobby, hobby_id)
    hobby.delete()
    return JsonResponse({'message': 'Hobby deleted successfully.'}, status=200)


@require_http_methods(['DELETE'])
@login_required
def delete_user_hobby(request: HttpRequest, hobby_id: int) -> HttpResponse:
    """
    View to delete a hobby from a specific user.
    """
    user = request.user
    hobby: Hobby = get_object_or_404(Hobby, id=hobby_id)

    if user.hobbies.filter(id=hobby_id).exists():
        user.hobbies.remove(hobby)
        return JsonResponse({'message': 'Hobby deleted successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Hobby not found in user\'s collection.'}, status=404)
