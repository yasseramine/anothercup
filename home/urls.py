from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('', views.about, name='about'),
    path('', views.contact, name='contact'),
    path('', views.pricing, name='pricing'),
    path('', views.delivery, name='delivery'),
    path('', views.assembly, name='assembly'),
    path('', views.returns, name='returns'),
] 