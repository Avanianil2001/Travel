from django import forms
from .models import *

# Create your forms here.

class Profile(forms.Form):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    mob_no = models.CharField(max_length=15)
    pro_pic = models.FileField()
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)