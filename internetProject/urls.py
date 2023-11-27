from django.urls import path
from internetProject import views
from django.contrib import admin
from django.urls import path, include

from internetProject.views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, \
    CustomPasswordResetCompleteView,PaymentView

app_name = 'internetProject'

urlpatterns = [
    path('', views.index, name='index'),
    path('coin-details/<str:coin_id>/<str:from_currency>/<str:to_currency>/', views.coin_details, name='coin_details'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('currency/<str:from_currency>/<str:to_currency>/', views.currency, name='currency'),
    path('currency_pay/<str:coin_id>/<str:from_currency>/<str:to_currency>/', views.currency_pay, name='currency_pay'),
    path('index_jk/', views.index_jk, name='index_jk'),
    # path('payment/', views.payment, name='payment'),
    path('payment/<str:from_currency>/<str:to_currency>/', PaymentView.as_view(), name='PaymentView'),
    path('about_us/', views.about_us, name='about_us'),
    path('faq/', views.faq, name='faq'),
    path('terms/', views.terms, name='terms'),
    path('request_form/', views.request_form, name='request_form'),
    path('complaint_form/', views.complaint_form, name='complaint_form'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),
    path('send_email/', views.send_email, name='send_email'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/<str:uidb64>/<slug:token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
