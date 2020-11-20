from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):

    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['class'] = "form-control"
        self.fields['password'].widget.attrs['class'] = "form-control"


class ShopperSignUpForm(forms.Form):
    username = UsernameField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class VendorSignUpForm(forms.Form):
    STORE_TYPES = (
        ("food", "Food"),
        ("clothes", "Clothes"),
        ("electonics", "Electonics")
    )

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    business_address = forms.CharField()
    business_phone = forms.CharField()
    store_type = forms.ChoiceField(choices=STORE_TYPES)
