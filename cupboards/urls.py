from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_cupboards, name='cupboards'),
    path('<cupboard_id>', views.cupboard_details, name='cupboard_details'),
] 