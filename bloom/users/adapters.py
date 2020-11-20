from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, sociallogin, form, commit=False):
        u = sociallogin.user
        if not u.username:
            u.username = u.email

        return super(AccountAdapter, self).save_user(request, sociallogin, form)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        role_type = request.session.get('role')
        u.role_type = role_type if role_type in ['1', '2'] else '2'
        if not u.username:
            u.username = u.email
        return super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
