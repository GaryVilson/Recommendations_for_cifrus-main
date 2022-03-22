from django.db import models
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40, null=False, unique=True)


class Subcategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=40, null=False)
    url = models.CharField(max_length=256, null=False)

    class Meta:
        unique_together = ('category', 'name')


class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    code = models.PositiveIntegerField(unique=True, null=True)
    name = models.CharField(max_length=256, null=False)
    price = models.FloatField(null=False, default=0)
    available = models.BooleanField(null=False, default=False)
    specifications = ArrayField(models.CharField(max_length=256), null=True)
    img = models.CharField(max_length=256)
