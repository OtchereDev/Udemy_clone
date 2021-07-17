
from payments.views import PaymentHandler, Webhook
from django.urls import path

app_name='payments'

urlpatterns = [
    path('webhook/',Webhook.as_view()),
    path('',PaymentHandler.as_view()),
]
