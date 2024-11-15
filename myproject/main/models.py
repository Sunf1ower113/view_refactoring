from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import CASCADE

class CustomUser(AbstractUser):
    search = models.OneToOneField('UserSearch', on_delete=models.CASCADE, null=True, blank=True)

class UserSearch(models.Model):
    search = models.CharField(max_length=255, blank=True, null=True)
    favorite = models.BooleanField(default=False)
    manager = models.ForeignKey('CustomUser', related_name='managed_users', null=True, blank=True, on_delete=models.SET_NULL)
    stage = models.IntegerField(null=True, blank=True)
    company = models.IntegerField(null=True, blank=True)
    customer = models.CharField(max_length=255, blank=True, null=True, default='')
    goal = models.BooleanField(default=False)

class Orders(models.Model):
    orderid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    reiting = models.IntegerField(default=0)
    goal = models.BooleanField(default=False)
    cityid = models.IntegerField(null=True, blank=True)
    stageid = models.IntegerField(null=True, blank=True)
    searchowners = models.CharField(max_length=255, blank=True, null=True)

class Comments(models.Model):
    orderid = models.ForeignKey(Orders, on_delete=models.CASCADE)
    createdat = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    istask = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

class Orderresponsible(models.Model):
    orderid = models.ForeignKey(Orders, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Ordercomresponsible(models.Model):
    orderid = models.ForeignKey(Orders, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class CustomersList(models.Model):
    orderid = models.ForeignKey(Orders, on_delete=models.CASCADE)
    customerid = models.ForeignKey('Customer', on_delete=models.CASCADE)

class Customer(models.Model):
    title = models.CharField(max_length=255)

class Costs(models.Model):
    cost_id = models.AutoField(primary_key=True)
    orderid = models.ForeignKey(Orders, on_delete=models.CASCADE)
    description = models.TextField()
    section = models.CharField(max_length=255)
    createdat = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Approvedlists(models.Model):
    cost_id = models.ForeignKey(Costs, on_delete=models.CASCADE)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

class Favorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)

