from django.urls import path
from internetProject import views
from django.contrib import admin
from django.urls import path, include

from internetProject.views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, \
    CustomPasswordResetCompleteView

app_name = 'internetProject'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('currency/<str:from_currency>/<str:to_currency>/', views.currency, name='currency'),
    path('index_jk/', views.index_jk, name='index_jk'),
    path('payment/', views.payment, name='payment'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
    