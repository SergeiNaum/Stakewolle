"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.decorators.cache import cache_page

from api_refs import views

urlpatterns = [
    path(
        "referral-code/",
        views.ReferralCodeCreateView.as_view(),
        name="create-referral-code",
    ),
    path(
        "referral-code/delete/",
        views.ReferralCodeDestroyView.as_view(),
        name="delete-referral-code",
    ),
    path(
        "referral-codes/<uuid:task_id>/result/",
        cache_page(10)(views.ShowUserReferalCode.as_view()),
        name="show-code",
    ),
    path(
        "referral-code/by-email/",
        views.ReferralCodeByEmailView.as_view(),
        name="referral-code-by-email",
    ),
    path("referrals/", views.ReferralListView.as_view(), name="referral_list"),
]
