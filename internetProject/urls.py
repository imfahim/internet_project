from django.urls import path
from internetProject import views

app_name = 'internetProject'

urlpatterns = [
    path('', views.index, name='index'),

]