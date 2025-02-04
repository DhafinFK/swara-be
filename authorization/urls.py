from django.urls import path
from .views import *

app_name = 'auth'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('google-auth/', GoogleLogin.as_view(), name='google')
]