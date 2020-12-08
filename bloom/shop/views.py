from django.shortcuts import render
from django.views.generic.base import View

from bloom.users.models import UserRole


class HomePage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_type == UserRole.BUSINESS:
            return render(request, 'pages/business_dashboard.html')

        return render(request, 'pages/home.html')

