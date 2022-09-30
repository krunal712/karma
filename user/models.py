import datetime
from django.db import models
from functools import wraps
from django.shortcuts import render,redirect
class Category(models.Model):
    name=models.CharField(max_length=50)
    thumbnailImage = models.ImageField(upload_to='images/', default="")

    def __str__(self):
        return self.name

class Products(models.Model):
    label=models.CharField(max_length=50)
    description=models.CharField(max_length=150)
    price=models.IntegerField()
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE,null=False)
    quantity=models.IntegerField()
    thumbnailImage = models.ImageField(upload_to='images/',default="")
    createdDate=models.DateField(auto_now_add=True)



    def __str__(self):
        return f"{self.label}"



class Users(models.Model):
    firstName=models.CharField(max_length=25)
    lastName=models.CharField(max_length=25)
    email=models.EmailField(max_length=30,null=False)
    mobileNumber=models.IntegerField()
    alternateNumber=models.IntegerField()
    createdDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.firstName


class Login(models.Model):
    email=models.EmailField(max_length=25)
    password=models.CharField(max_length=100)
    login_user_id=models.ForeignKey(Users,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Login"

class ShippingAddress(models.Model):
    addressLine1=models.CharField(max_length=50)
    addressLine2= models.CharField(max_length=50)
    city=models.CharField(max_length=25)
    state=models.CharField(max_length=25)
    country=models.CharField(max_length=25)
    shippingAddress_user_id=models.ForeignKey(Users,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.addressLine1
    class Meta:
        verbose_name_plural = "ShippingAddress"
# Create your models here.
class Cart(models.Model):
    product=models.ForeignKey(Products,null=False,on_delete=models.CASCADE, related_name='products')
    user=models.ForeignKey(Login,null=False,on_delete=models.CASCADE, related_name='users')
    quantity=models.IntegerField()
    createdDate = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.product}"


def login_required(f):
    @wraps(f)
    def _wrapped_view(request,*args,**kwargs):
        # for i,j in request.session:
        #     print(i,j)
        if 'is_loged_in' in request.session:
            return f(request, *args, **kwargs)
        else:
            return redirect("/login",method='GET')
    return _wrapped_view