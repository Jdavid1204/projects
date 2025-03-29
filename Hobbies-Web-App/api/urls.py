"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    main_spa,
    login_view,
    signup_view,
    logout_view,
    get_hobbies,
    get_users,
    get_user,
    update_user,
    get_similar_users,
    accept_friend_request,
    send_friend_request,
    decline_friend_request,
    add_hobby,
    update_hobby,
    delete_hobby,
    delete_user_hobby,
)

urlpatterns = [
    path('', main_spa),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/logout/', logout_view, name='logout'),
    path('hobbies/', get_hobbies, name='get_hobbies'),
    path('users/', get_users, name='get_users'),
    path('users/user-info/', get_user, name='get_current_user'),
    path('users/user-info/<int:user_id>/', get_user, name='get_user'),
    path('users/update/', update_user, name='get_user'),
    path('users/similar/', get_similar_users, name='get_similar_users'),
    path('users/request/<int:receiver_id>/', send_friend_request, name='send_friend_request'),
    path('users/request/accept/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('users/request/decline/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
    path('hobbies/add/', add_hobby, name='add_hobby'),
    path('hobbies/update/<int:hobby_id>/', update_hobby, name='update_hobbies'),
    path('hobbies/delete/<int:hobby_id>/', delete_hobby, name='delete_hobbies'),
    path('users/hobbies/delete/<int:hobby_id>/', delete_user_hobby, name='delete_user_hobby'),
]
