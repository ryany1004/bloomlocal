import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from bloom.order.cart import Cart
from bloom.order.models import Order
from bloom.order.payment import transfer_to_connected_accounts

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderOverviewPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/shop/order-overview.html', {"page": 'order-overview'})


class OrderSuccessPage(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, uuid=kwargs['uuid'])
        cart = Cart(request)
        cart.clear()
        return render(request, 'pages/shop/order-success.html', {"page": 'order-success', 'order': order})


class OrderCanceledPage(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, uuid=kwargs['uuid'])
        if order.status == Order.Status.PENDING:
            order.status = Order.Status.CANCELED
            order.save()
        return render(request, 'pages/shop/order-canceled.html', {"page": 'order-success', 'order': order})


@method_decorator(csrf_exempt, name='dispatch')
class OrderHooksPage(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET_KEY
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400, content=str(e))
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400, content=str(e))

        print('Event type {}'.format(event.type))

        return self.handle_event(event)

    def handle_event(self, event):
        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object  # contains a stripe.PaymentIntent

            order = Order.objects.filter(payment_intent=payment_intent.id).first()
            if order:
                order.status = Order.Status.SUCCEED
                order.save()

                transfer_to_connected_accounts(order)

        elif event.type == "payment_intent.canceled":
            payment_intent = event.data.object
            order = Order.objects.filter(payment_intent=payment_intent.id).first()
            if order:
                order.status = Order.Status.CANCELED
                order.save()

            print('PaymentIntent was canceled!')
        elif event.type == 'account.updated':
            acct = event.data.object  # contains a stripe.PaymentMethod
            user = User.objects.filter(stripe_account_id=acct.id).first()
            if acct.charges_enabled:
                if user:
                    user.charges_enabled = True
                    user.save()
                    print('Account {} was submitted'.format(acct.id))
                else:
                    print("User with {} was not found".format(acct.id))
            else:
                if user and user.charges_enabled:
                    user.charges_enabled = False
                    user.save()
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AccountHooksPage(OrderHooksPage):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_CONNECTED_ACCOUNT_KEY
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400, content=str(e))
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400, content=str(e))

        print('Event type {}'.format(event.type))

        return self.handle_event(event)
