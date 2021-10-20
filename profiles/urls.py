from django.urls import path
from . import views


urlpatterns = [
    path('', views.my_cupboards, name='my_cupboards'),
] 