from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_cupboards, name='cupboards'),
    path('<int:cupboard_id>', views.cupboard_details, name='cupboard_details'),
    path('<int:cupboard_id>/<material_id>/<type_id>', views.calculated_cupboard,
         name='calculated_cupboard'),
    path('add/', views.add_design_material, name='add_design_material'),
    path('add_design/', views.add_design, name='add_design'),
    path('add_material/', views.add_material, name='add_material'),
]