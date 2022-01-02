from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout,get_user_model
from django.contrib.auth.decorators import login_required

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
                    newUser.set_password(userData["password"])
                    #set email to username
                    newUser.username=userData['email']
                    newUser.save()
                    
                    #set other data to profie model
                    
                    profile = Profile()
                    profile.user = newUser
                    profile.name = userData['name']
                    profile.email = userData['email']
                    profile.password = userData['password']
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

    

    return render(req,"register.html",context)

def login_view(req):
    next = req.GET.get('next')
    context = {"errors":[]}
    if req.method == "POST":
        print("hi")
        #authenticate user
        user = authenticate(username=req.POST['email'],password=req.POST['password'])
        print(user)
        if user is not None:
            #login user
            login(req,user)
            if next:
                return redirect(next)
            else:
                return redirect("/profile")
        else:
            context["errors"].append("Invalid login!")
            

        
    
    return render(req,'login.html',context)


@login_required(login_url="/login")
def profile(req):
    
    if req.method=="POST":
        #get post data to userData dict
        userData = {
            "name":req.POST['name'],
            "bd":req.POST['bd'],
            "pob":req.POST['pob'],
            "sex":req.POST['sex'],
            "email":req.POST['email']
        }

        try:
            user = req.user
            user.first_name = userData['name']
            #set email to username
            user.username=userData['email']
            user.save()
            #set other data to profie model
            profile = Profile.objects.filter(user=user).first()
            profile.name = userData['name']
            profile.email = userData['email']
            profile.password = userData['password']
            profile.birthday = userData["bd"]
            profile.placeOfBirth = userData["pob"]
            profile.sex = userData["sex"]
            profile.save()
        except Exception as e:
            print(e)#log error
                
    #get profile data
    profile = Profile.objects.filter(user=req.user).first()
    
    return render(req,"profile.html",{"profile":profile})


def logout_view(req):
    logout(req)
    return redirect("/login")

@login_required(login_url="/login")
def deleteAccount(req):
    user = req.user
    logout(req)
    user.delete()
    return redirect("/")