from django.urls import path, include

from currency_exchange import views

urlpatterns = [
    path(r'currency/<str:from_currency>/<str:to_currency>/', views.currency, name='currency'),
]