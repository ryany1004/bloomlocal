import stripe
from allauth.account.views import SignupView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.base import View

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def _generate_account_link(account_id, origin):
    account_link = stripe.AccountLink.create(
        type='account_onboarding',
        account=account_id,
        refresh_url=f'{origin}/users/stripe/refresh/',
        return_url=f'{origin}/users/details/',
    )
    return account_link.url


class StripConnectView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        account = stripe.Account.create(type='express')
        # Store the account ID.
        request.session['account_id'] = account.id

        origin = request.headers['origin']

        account_link_url = _generate_account_link(account.id, origin)
        try:
            user = request.user
            user.stripe_account_id = account.id
            user.save()

            return JsonResponse({'url': account_link_url})
        except Exception as e:
            return JsonResponse(error=str(e)), 403


class StripAccountRefreshView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'account_id' not in request.session:
            return redirect('/')

        account_id = request.session['account_id']

        origin = ('https://' if request.is_secure else 'http://') + request.headers['host']
        account_link_url = _generate_account_link(account_id, origin)
        return redirect(account_link_url)

