from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey

User = get_user_model()

class Profile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=200)
    email=models.EmailField()
    password = models.CharField(max_length=200)
    birthday = models.DateField()
    placeOfBirth = models.CharField(max_length=200)
    sex =models.CharField(max_length=10)
    isAnswered = models.BooleanField(default=False)
    lastRecommendation = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return str(self.name+" | "+self.email)

class Question(models.Model):
    text = models.CharField(max_length=1000,null=False,blank=False)
    def __str__(self):
        return str(self.text)
    

class Answer(models.Model):
    text = models.CharField(max_length=500,null=False,blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.text)

class UserAnswer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    q = models.ForeignKey(Question,on_delete=models.CASCADE)
    a = models.ForeignKey(Answer,on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return str(self.user)
    
    