from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model

from main.models import Profile


User = get_user_model()



def register(req):
    
    context = {"errors":[],"msg":[]}
    
    if req.method == "POST":
        #get post data to userData dict
        userData = {
            "name":req.POST['name'],
            "bd":req.POST['bd'],
            "pob":req.POST['pob'],
            "sex":req.POST['sex'],
            "email":req.POST['email'],
            "password":req.POST['password']
        }

        #check if password is confirmed
        if(req.POST["password"] == req.POST["re_password"]):
            #check email already exists
            e = User.objects.filter(email=userData['email'])
            if e.exists() == False:
                try:
                    newUser = User()
                    newUser.first_name = userData['name']
                    newUser.email=userData['email']
                    newUser.set_password(userData["password"])
                    #set email to username
                    newUser.username=userData['email']
                    newUser.save()
                    #set other data to profie model
                    
                    profile = Profile()
                    profile.user = newUser
                    profile.birthday = userData["bd"]
                    profile.placeOfBirth = userData["pob"]
                    profile.sex = userData["sex"]
                    profile.save()
                    
                    context["msg"].append("User added!")
                except Exception as e:
                    print(e)#log error
                    context["errors"].append("something wrong!")
                    
                    
                
            else:
                context["errors"].append("This E-mail already exists!")
        
        pass
        
    
    # DB.append()
    
    return render(req,"register.html",context)
