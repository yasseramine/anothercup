from django.db import models

# Create your models here.


class Material(models.Model):

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)
    price_per_m2 = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Type(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Cupboard(models.Model):

    design_id = models.CharField(max_length=6)
    type = models.ForeignKey('Type', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    material = models.ForeignKey('Material', null=True, blank=False,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    description = models.TextField()
    design_surcharge = models.DecimalField(max_digits=6, decimal_places=2)
    example_price = models.DecimalField(max_digits=6, decimal_places=2)
    main_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name 


class Image(models.Model):
    file_name = models.ImageField(null=True, blank=True)
    cupboard = models.ForeignKey(Cupboard, on_delete=models.CASCADE)
    main_image = models.BooleanField (null=False, blank=False, default=False)

    def __str__(self):
        return self.file_name.path

