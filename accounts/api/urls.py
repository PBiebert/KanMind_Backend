from django.urls import path
from .views import RegistrationView, LoginView, FindUserView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('email-check/', FindUserView.as_view())
]
