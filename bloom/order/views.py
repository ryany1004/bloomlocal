import stripe
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from bloom.order.models import Order


class OrderOverviewPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/shop/order-overview.html', {"page": 'order-overview'})


class OrderSuccessPage(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, uuid=kwargs['uuid'])
        return render(request, 'pages/shop/order-success.html', {"page": 'order-success', 'order': order})


class OrderCanceledPage(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, uuid=kwargs['uuid'])
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
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object  # contains a stripe.PaymentIntent

            order = Order.objects.get(payment_intent=payment_intent.id)
            order.status = Order.Status.SUCCEED
            order.save()

            print('PaymentIntent was successful!')
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object  # contains a stripe.PaymentMethod
            print('PaymentMethod was attached to a Customer!')
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)
