from django.test import TestCase
from django.urls import reverse,resolve
from app.views import *

class TestURLS(TestCase):
    def setUp(self):
        self.homeurl = reverse('rooms')
        self.signinurl = reverse('signin')
        self.singupurl = reverse('signup')
        self.roomurl = reverse('room',args=['slug'])
        self.createurl = reverse('createroom')
        self.enterurl = reverse('enter',args=['str'])

    def test_urls(self):
        self.assertEquals(resolve(self.homeurl).func,home)
        self.assertEquals(resolve(self.signinurl).func,signin)
        self.assertEquals(resolve(self.singupurl).func,signup)
        self.assertEquals(resolve(self.roomurl).func,room)
        self.assertEquals(resolve(self.createurl).func,create_room)
        self.assertEquals(resolve(self.enterurl).func,enter)
        