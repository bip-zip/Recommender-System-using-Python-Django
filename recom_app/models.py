from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category=models.CharField(max_length=20)

    def __str__(self):
        return self.category

class Product(models.Model):
    name=models.CharField(max_length=200, null=True)
    price=models.FloatField()
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    descrption=models.TextField(max_length=2000,blank=True, null=True)

    def __str__(self):
        return self.name

class OrderItems(models.Model):
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    customer= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.product)

    

from datetime import datetime
class SearchHistory(models.Model):
    query= models.TextField(blank=True, null=True)
    customer= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.query)

from django.core.validators import MaxValueValidator, MinValueValidator
class Rating(models.Model):
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    rating=models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.product.name
    
