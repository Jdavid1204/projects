from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hobby, FriendRequest


class FriendRequestInline(admin.TabularInline):
    """
    Inline admin for managing sent and received friend requests for a user.
    """
    model = FriendRequest
    fk_name = 'sender'
    extra = 0


class ReceivedFriendRequestInline(admin.TabularInline):
    """
    Inline admin for managing received friend requests.
    """
    model = FriendRequest
    fk_name = 'receiver'  # This displays received friend requests
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for CustomUser with friends and friend requests management.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth', 'hobbies', 'friends')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth', 'hobbies')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('hobbies', 'friends')
    inlines = [FriendRequestInline, ReceivedFriendRequestInline]

admin.site.register(Hobby)
admin.site.register(FriendRequest)