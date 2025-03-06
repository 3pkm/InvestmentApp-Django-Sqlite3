from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Investment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to User
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Links to Product
    investment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.customer.username} - {self.product.name} - ${self.investment_amount}"