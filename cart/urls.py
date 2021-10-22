from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('<cupboard_id>/<code>',
         views.add_to_cart, name='add_to_cart'),
] 