from django.db import models

# Create your models here.

class Register(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=15, blank=True, null=True)  # Optional
    email = models.EmailField()
    mob_no = models.CharField(max_length=15)  # Change to CharField to accommodate larger numbers
    pro_pic = models.FileField()
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class BlogPost(models.Model):
    user_details = models.ForeignKey(Register,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    place = models.CharField(max_length=30)
    content = models.TextField()
    image = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    user_details = models.ForeignKey(Register,models.CASCADE)
    feedback = models.TextField()