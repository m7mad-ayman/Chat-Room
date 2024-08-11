import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import *

class NormalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.groupname = "user_%s" % self.room_name
        await self.channel_layer.group_add(self.groupname,self.channel_name)
        await self.accept()
        
    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
            )
    async def receive(self,text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        roomname = data['roomname']
        await self.channel_layer.group_send(
            self.groupname,{
                'type':'chat_message',
                'message':message,
                'username':username,
                'roomname':roomname,
            })
        await self.save_message(message,username,roomname)
        
    async def chat_message(self,event):
        message = event['message']
        username = event['username']
        roomname = event['roomname']
        await self.send(text_data=json.dumps({
                'message':message,
                'username':username,
                'roomname':roomname,
            }))
    @sync_to_async    
    def save_message(self,message,username,room):
        user = User.objects.get(username=username)
        room = ChatRoom.objects.get(slug=room)
        save = ChatMessage(user=user,room=room,content=message)
        if not save == None:
            save.save()
        else: pass 