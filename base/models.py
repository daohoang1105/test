# from pydoc import describe
from distutils.command.upload import upload
from email.policy import default
from pickle import TRUE
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from numpy import product
# # Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=TRUE)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [] 
    
    role_choice = ((0, "Guest"),(1,"Distributor"),(2,"Sungrow"),(3, "ADMIN"),(4,"SUPER USER"))
    role = models.IntegerField(choices = role_choice, default=0)

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User,related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    product_serial_number = models.CharField(max_length=11, null=False, blank=False)
    product_model = models.CharField( max_length=10, null=False, blank=False)
    date_of_installation = models.DateTimeField(null=False, blank=False)

    company = models.CharField(max_length=100, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=False, blank=True)
    contact_number = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    other_recipients = models.CharField(max_length=100, null=True, blank=True)
    site_address = models.CharField(max_length=100, null=True, blank=True)
    shipping_address = models.CharField(max_length=100, null=True, blank=True)

    warranty_choice = (("Valid", "Valid"),("Invalid","Invalid"),("Warranty with fee","Warranty with fee"),("Waiting...","Waiting..."))
    inoutwarranty = models.CharField(max_length=100,choices=warranty_choice,default="Waiting...")

    role_choice = ((0, "Recieved Mail"),(1,"Inspection"),(2,"Warranty clasification"),(3, "Repairing"),(4,"Testing"),(5,"Delivering"),(6,"CLOSED"))
    role = models.IntegerField(choices = role_choice, default=0)
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    images = models.ImageField(upload_to='img', null=False, default=None)
    file = models.FileField(upload_to='file', null=False, default=None)

    class Meta:
        ordering = ['-updated', '-created']
 
    def __str__(self):
        return f"{self.body[0:50],{self.images},{self.file}}"

    # def selfDestruction(self):
    #     if self.body == None and self.images == None and self.file == None:
    #         self.delete()

class Warranty(models.Model):
    product_serial_number = models.CharField(max_length=11, null=False, blank=False)
    product_model = models.CharField( max_length=10, null=False, blank=False)
    date_of_installation = models.DateTimeField(null=False, blank=False)

    company = models.CharField(max_length=100, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=False, blank=True)
    contact_number = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    other_recipients = models.CharField(max_length=100, null=True, blank=True)
    site_address = models.CharField(max_length=100, null=True, blank=True)
    shipping_address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.product_serial_number)

class BMS(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    
    SOC = models.CharField(max_length=100, null=True, blank=True)
    Vol = models.CharField(max_length=100, null=True, blank=True)
    Amp = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.owner)