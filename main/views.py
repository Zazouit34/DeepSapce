from operator import indexOf
from django import http
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout,get_user_model
from django.contrib.auth.decorators import login_required

from main.models import Answer, Profile, Question, UserAnswer

import random


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

@login_required(login_url="/login")
def questions(req):
    id = int(req.GET['id'])
    qus = Question.objects.all()
    
    try:
        qid = req.GET['qid']
        if qid != None:
            aid = req.GET['answer']
            ua = UserAnswer()
            ua.user = req.user
            ua.q = Question.objects.get(id=qid)
            ua.a = Answer.objects.get(id=aid)
            ua.save()
    except:
        pass
    
    
    
    if id == -1:
        return redirect("/thanks")
        

    
    if id < len(qus):
        q = qus[id]
        ans = Answer.objects.filter(question = q)
        if id < len(qus)-1:
            next = id + 1
        else:
            next = -1
        context = {
            "data":{
                "q":q,
                "ans":ans,
                "next":next
            }
        }
        return render(req,"questions.html",context)
    else:
        return redirect("/profile")

@login_required(login_url="/login")
def thanks(req):
    txts = [
        "Read: The subtle art of not giving a fuck from Mark Manson. You will see the tings in a completely different way and it will help you to understand the people around you.",
        "Read: I know how she does it from Laura Vanderkam. It will show you how to increase your productivity and manage your time management.",
        "Find peace in yoga and meditation. It exercises the memory and helps you to focus.",
        "Sing in the Shower. Splash your music all around! It reduces stress and helps you to relax",
        "Eat your favorite food. It will improve your mood.",
        "Take your bag pack and go on a short trip to be more happier, calmer, and more energized.",
        "Have a walking meeting with your best friend in the nature. Try to breathe more deeply, drawing more air deep into the bottom of your lungs this will lead to a healthier you.",
        "Challenge yourself with something new. It will improve your mental health, but also affect your personal well being.",
        "Practice being mindful. It will help you to De-Stress.",
        "Have a beauty/Spa day. It releases Serotonin and Dopamine.",
        "Clean your apartment. It will be more comfortable, and it also will help in making your home more welcoming.",
        "Meet new people. Good practice to sharpen your social skills. And maybe you find your next best friend or your soul mate!",
        
    ]
    txt = random.choice(txts)
    index = txts.index(txt)
    profile = Profile.objects.get(user=req.user)
    profile.lastRecommendation = index
    profile.save()
    

    return render(req,"thanks.html",{"txt":txt})

@login_required(login_url="/login")
def getLastRecommendation(req):
    
    txts = [
        "Read: The subtle art of not giving a fuck from Mark Manson. You will see the tings in a completely different way and it will help you to understand the people around you.",
        "Read: I know how she does it from Laura Vanderkam. It will show you how to increase your productivity and manage your time management.",
        "Find peace in yoga and meditation. It exercises the memory and helps you to focus.",
        "Sing in the Shower. Splash your music all around! It reduces stress and helps you to relax",
        "Eat your favorite food. It will improve your mood.",
        "Take your bag pack and go on a short trip to be more happier, calmer, and more energized.",
        "Have a walking meeting with your best friend in the nature. Try to breathe more deeply, drawing more air deep into the bottom of your lungs this will lead to a healthier you.",
        "Challenge yourself with something new. It will improve your mental health, but also affect your personal well being.",
        "Practice being mindful. It will help you to De-Stress.",
        "Have a beauty/Spa day. It releases Serotonin and Dopamine.",
        "Clean your apartment. It will be more comfortable, and it also will help in making your home more welcoming.",
        "Meet new people. Good practice to sharpen your social skills. And maybe you find your next best friend or your soul mate!",
        
    ]
    
    profile = Profile.objects.get(user=req.user)
    index = profile.lastRecommendation
    txt = ""
    if index != None:
        txt = txts[index]
        
    return render(req,"last-recommendation.html",{"txt":txt})