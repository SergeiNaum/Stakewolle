from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('register/refer/', views.RegisterWithReferralView.as_view()),

]
