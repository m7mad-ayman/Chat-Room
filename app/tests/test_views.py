from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.views import *
from app.models import ChatRoom , LogedIn

class TestURLS(TestCase):
    def setUp(self):
        self.homeurl = reverse('rooms')
        self.signinurl = reverse('signin')
        self.singupurl = reverse('signup')
        self.roomurl = reverse('room',args=['test'])
        self.createurl = reverse('createroom')
        self.logouturl = reverse('logout')
        self.client = Client()
        self.user = User.objects.create(username="tester")
        self.user.set_password('test1234')
        self.user.save()
        self.room = ChatRoom(admin=self.user,name='test',slug="test",password='1234')
        self.room.save()

    def test_login(self):
        response1 = self.client.get(self.signinurl)
        self.assertTemplateUsed(response1,'signin.html')
        response2=self.client.post(self.signinurl,{'username':'tester','password':'test1234'})
        self.assertEquals(response2.status_code,302)
        response3=self.client.post(self.signinurl,{'username':'tester','password':'wrongpassword'})
        self.assertEquals(response3.context['message'],"username or password isn't correct")
    
    def test_signup(self):
        response1 = self.client.get(self.singupurl)
        self.assertTemplateUsed(response1,'signup.html')

        response2 = self.client.post(self.singupurl,{'username':'tester','email':'test@gmail.com','password':'test1234','confirm':'test1234'})
        self.assertEquals(response2.context['message'],"username or email is already taken")

        response3 = self.client.post(self.singupurl,{'username':'test','email':'testgmail.com','password':'test1234','confirm':'test1234'})
        self.assertEquals(response3.context['message'],"email isn't valid")
        
        response4 = self.client.post(self.singupurl,{'username':'test','email':'test@gmail.com','password':'test1234','confirm':'test12'})
        self.assertEquals(response4.context['message'],"passwords don't match")

        response5 = self.client.post(self.singupurl,{'username':'test','email':'test@gmail.com','password':'12345678','confirm':'12345678'})
        self.assertEquals(response5.context['message'],"password must contain letters and numbers , 8 at least")

        response6 = self.client.post(self.singupurl,{'username':'test','email':'test@gmail.com','password':'test1234','confirm':'test1234'})
        self.assertEquals(response6.status_code,302)
    
    def test_logout(self):
        self.client.login(username='tester',password='test1234')
        response= self.client.get(self.logouturl)
        self.assertEquals(response.status_code,302)

    def test_home(self):
        self.client.login(username='tester',password='test1234')
        response =self.client.get(self.homeurl)
        self.assertTemplateUsed(response,'home.html')

    def test_room(self):
        self.client.login(username='tester',password='test1234')
        response1 = self.client.get(self.roomurl)
        self.assertTemplateUsed(response1,'password.html')

        LogedIn(user=self.user,room=self.room).save()
        response2 = self.client.get(self.roomurl)
        self.assertTemplateUsed(response2,'room.html')

    def test_enter(self):
        self.client.login(username='tester',password='test1234')
        response1 = self.client.post(reverse('enter',args=[str(self.room.id)]),{"password":'1234'})
        self.assertEquals(response1.status_code,302)

        response2 = self.client.post(reverse('enter',args=[str(self.room.id)]),{"password":'123'})
        self.assertTemplateUsed(response2,'password.html')
    
    def test_createroom(self):
        self.client.login(username='tester',password='test1234')
        response1 = self.client.get(self.createurl)
        self.assertTemplateUsed(response1,'createroom.html')

        response2 = self.client.post(self.createurl,{"roomname":"test",'password':'1234'})
        self.assertEquals(response2.context['message'],'roomname already exist')

        response3 = self.client.post(self.createurl,{"roomname":"test2",'password':'1234'})
        self.assertEquals(response3.status_code,302)
