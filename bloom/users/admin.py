from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from bloom.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("phone_number",)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "is_superuser", 'charges_enabled', 'stripe_account_id']
    search_fields = ["first_name", 'last_name']
