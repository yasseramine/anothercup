from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_cupboards, name='cupboards'),
    path('<int:cupboard_id>', views.cupboard_details, name='cupboard_details'),
    path('<int:cupboard_id>/<material_id>/<type_id>', views.calculated_cupboard,
         name='calculated_cupboard'),
    path('add_design/', views.add_design, name='add_design'),
    path('add_material/', views.add_material, name='add_material'),
    path('edit_design/<int:cupboard_id>', views.edit_design, name='edit_design'),
    path('edit_material/<int:material_id>', views.edit_material, name='edit_material'),
    path('materials/', views.list_materials, name='materials'),
    path('delete_material/<int:material_id>', views.delete_material, name='delete_material'),
    path('delete_design/<int:cupboard_id>', views.delete_design, name='delete_design'),
]