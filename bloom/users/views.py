import binascii
import hashlib
import hmac
import os

import shopify
import stripe
from allauth.account.views import SignupView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.base import View

from bloom.users.forms import ShopifyConfigForm
from bloom.users.models import ShopifyConfig
from bloom.users.shopify import create_session, create_permission_url

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['page'] = 'profile'
        return context


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
        refresh_url='{}{}'.format(origin, reverse("users:stripe_refresh")),
        return_url='{}{}'.format(origin, reverse("users:stripe-integration")),
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


class StripeSettingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/connect_stripe.html', context={"page": 'stripe'})


class ShopifySettingView(LoginRequiredMixin, UpdateView):
    model = ShopifyConfig
    template_name = 'users/connect_shopify.html'
    form_class = ShopifyConfigForm
    context_object_name = 'shopify'

    def get_object(self, queryset=None):
        return self.request.user.get_shopify_config()

    def get_success_url(self) -> str:
        return reverse("users:shopify-integration")

    def get_context_data(self, **kwargs):
        context = super(ShopifySettingView, self).get_context_data(**kwargs)
        context["page"] = 'shopify'
        context['redirect_url'] = self.request.build_absolute_uri(reverse("users:shopify-callback"))
        return context

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "Your key is verified.")
        return redirect(self.get_success_url())

    # def form_valid(self, form):
    #     obj = form.save()
    #     redirect_uri = self.request.build_absolute_uri(reverse('users:shopify-callback'))
    #     state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    #     self.request.session['shopify_oauth_state_param'] = state
    #     url = create_permission_url(obj, state=state, redirect_uri=redirect_uri)
    #     return redirect(url)


class ShopifyCallbackView(View):
    def get(self, request, *args, **kwargs):
        config = self.request.user.get_shopify_config()

        params = request.GET.dict()
        if request.session['shopify_oauth_state_param'] != params['state']:
            messages.error(request, 'Anti-forgery state token does not match the initial request.')
            return redirect(reverse('users:shopify-integration'))
        else:
            # request.session.pop('shopify_oauth_state_param', None)
            pass

        myhmac = params.pop('hmac')

        line = '&'.join([
            '%s=%s' % (key, value)
            for key, value in sorted(params.items())
        ])
        h = hmac.new(config.secret_key.encode('utf-8'), line.encode('utf-8'), hashlib.sha256)
        if not hmac.compare_digest(h.hexdigest(), myhmac):
            messages.error(request, "Could not verify a secure login")
            return redirect(reverse('users:shopify-integration'))
        session = create_session(config.shop_url, config.api_key, config.secret_key)
        try:
            access_token = session.request_token(request.GET)
            config.access_token = access_token
            config.save()
        except Exception:
            config.access_token = None
            config.save()
            messages.error(request, "Could not verify a secure login")
            return redirect(reverse('users:shopify-integration'))

        messages.info(request, "Logged in to shopify store.")
        return redirect(reverse('users:shopify-integration'))


