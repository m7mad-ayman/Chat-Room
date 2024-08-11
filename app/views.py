from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from .models import *
import re
def signin(request):
    if request.method =="POST":
        if not (request.POST["username"] == '') or not (request.POST["password"]=='') :
           if "@" in request.POST['username']:
               username = request.POST["username"]
               password = request.POST["password"]
               user=auth.authenticate(email = request.POST['username'],password=request.POST['password'])
           else:
               username = request.POST["username"]
               password = request.POST["password"] 
               user=auth.authenticate(username = username,password=password)
           if user != None:
               auth.login(request,user)
               return redirect("/")
           else:
               return render(request,"signin.html",{"message":"username or password isn't correct"})
        else:
           return render(request,"signin.html",{"message":"username or password can't be empty"})
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,"signin.html")

def signup(request):
    if request.method=="POST":
        if not (request.POST["username"] == '') or not (request.POST["email"]=='') or not (request.POST["password"]=='') or not (request.POST["confirm"]=='') :
            if not User.objects.filter(username = request.POST.get('username')).exists() and (not User.objects.filter(email = request.POST.get('email')).exists()): 
                if not ('@' in request.POST.get('username')) or not (' ' in request.POST.get('username')):
                    if "@" in str(request.POST.get('email')): 
                        
                        if request.POST.get('password') == request.POST.get('confirm'):
                            if len(request.POST.get('password'))>=8 and (not str(request.POST.get('password')).isalpha()) and not(str(request.POST.get('password')).isnumeric()) :
                                user=User.objects.create_user(username =request.POST['username'],email=request.POST['email'])
                                user.set_password(request.POST['password'])
                                user.save()
                                if user != None:
                                    return redirect("/signin")
                            else:
                                return render(request,"signup.html",{"message":"password must contain letters and numbers , 8 at least"})
                        else:
                            return render(request,"signup.html",{"message":"passwords don't match"})
                    else:
                        return render(request,"signup.html",{"message":"email isn't valid"})
                else:
                    return render(request,"signup.html",{"message":"not valid username"})
            
            else:
                return render(request,"signup.html",{"message":"username or email is already taken"})
        else :
            return render(request,"createroom.html",{'message':"Don't leave any field empty"})  
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,"signup.html")

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect("/signin/")


   
@login_required(login_url='signin')
def home(request):
    rooms = ChatRoom.objects.order_by('-created_at')
    return render(request,"home.html",{'rooms':rooms})

@login_required(login_url='signin')
def room(request,slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    user= request.user
    
    if LogedIn.objects.filter(user=user,room=chatroom).exists():
        chatroom = ChatRoom.objects.get(slug=slug)
        chatmessages = ChatMessage.objects.filter(room = chatroom)
        return render(request,"room.html",{"chatroom":chatroom,"chatmessages":chatmessages})
    else : 
        return render(request,"password.html",{"chatroom":chatroom})

@login_required(login_url='signin')
def enter(request,id):
    chatroom = ChatRoom.objects.get(id=id)
    user=request.user
    if request.method == "POST":
        if  not (request.POST["password"]==''):
            if request.POST.get("password") == chatroom.password : 
                LogedIn.objects.create(user=user,room=chatroom).save()
                return redirect("/room/{0}/".format(chatroom.name))
            else:
                return render(request,"password.html",{"chatroom":chatroom,"message":"password is not correct"})
        else:
            return render(request,"password.html",{'message':"Don't leave any field empty"})  
    
@login_required(login_url='signin')
def create_room(request):
    if request.method == "GET":
        return render(request,"createroom.html")
    
    elif request.method == "POST":
        if not (request.POST["roomname"]=='') or not (request.POST["password"]==''):
            if not (ChatRoom.objects.filter(name = request.POST.get("roomname").replace(" ","_")).exists()):
                room = ChatRoom(name = request.POST.get("roomname").replace(" ","_"),slug=request.POST.get("roomname").replace(" ","_"),admin=request.user)
                room.password = request.POST["password"]
                room.save()
                return redirect("/")
            else :
                return render(request,"createroom.html",{'message':'roomname already exist'})
        else :
            return render(request,"createroom.html",{'message':"Don't leave any field empty"})  

@login_required(login_url='signin')
def delete_room(request,id):
    room = ChatRoom.objects.get(id=id)
    room.delete()
    return redirect('/')

@login_required(login_url='signin')
def change_password(request,id):
    room = ChatRoom.objects.get(id=id)
    if request.method == "GET":

        return render(request,'change_pass.html',{'chatroom':room})
    elif request.method == "POST":
        if  not (request.POST["password"]==''):
            
            room.password = request.POST['password']
            room.save()
            LogedIn.objects.filter(room = room).delete()
            return redirect('/room/{0}/'.format(room.name))
        else:
            return render(request,"change_pass.html",{'message':"Don't leave any field empty",'chatroom':room})