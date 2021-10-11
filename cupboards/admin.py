from django.contrib import admin
from .models import Material, Design

# Register your models here.

class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'material_id',
        'name',
        'price_per_m2',
    )

    ordering = ('display_name',)


class DesignAdmin(admin.ModelAdmin):
    list_display = (
        'design_id',
        'name',
        'type',
        'design_surcharge',
        'example_price',
        'main_image'
    )

    ordering = ('design_id',)


admin.site.register(Material, MaterialAdmin)
admin.site.register(Design, DesignAdmin)