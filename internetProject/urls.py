from django.urls import path
from internetProject import views
from django.contrib import admin
from django.urls import path, include

app_name = 'internetProject'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
]
    