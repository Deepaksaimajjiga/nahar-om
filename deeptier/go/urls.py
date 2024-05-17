from django.urls import path, include
from .views import *

# All these APIs are for sellers

urlpatterns = [
    path("sample/", SampleView.as_view(), name="generate_otp"),
]