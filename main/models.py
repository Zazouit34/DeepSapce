from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    birthday = models.DateField()
    placeOfBirth = models.CharField(max_length=200)
    sex =models.CharField(max_length=10)
