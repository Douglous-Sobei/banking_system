from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("kyc-reg/", views.kyc_registration, name="kyc-reg"),
]
