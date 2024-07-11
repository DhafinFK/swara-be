from django.urls import path
from .views import *

app_name = 'angkat_isu'

urlpatterns = [
    path('', AngkatIsuAPI.as_view(), name="angkat-isu"),
]