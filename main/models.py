from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=200)
    email=models.EmailField()
    password = models.CharField(max_length=200)
    birthday = models.DateField()
    placeOfBirth = models.CharField(max_length=200)
    sex =models.CharField(max_length=10)
    
    def __str__(self):
        return str(self.name+" | "+self.email)
