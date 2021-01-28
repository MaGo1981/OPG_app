from django.db import models
from django.contrib.auth.models import User



class ProductCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"



class Opg(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"



class Product(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)
    opg_id = models.ForeignKey(Opg, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.name}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(null=True, blank=True)
    opg_id = models.ForeignKey(Opg, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"