from django.test import TestCase
from app.models import *
from django.contrib.auth.models import User
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import path
from app.consumers import NormalConsumer
from channels.db import database_sync_to_async


class TestConsumers(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester",password="test1234")
        self.room = ChatRoom(admin=self.user,name='test',slug='test')
        self.room.save()
    async def test_consumers(self):
        application = URLRouter([
        path("ws/<str:room_name>/", NormalConsumer.as_asgi()),
        ])
        communicator = WebsocketCommunicator(application, "/ws/test/")
        connected , subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.send_json_to({
                'type':'chat_message',
                'message':"testing consumers",
                'username':"tester",
                'roomname':'test',
            })
        response =  await communicator.receive_json_from()
        self.assertTrue(response.get('message'),'testing consumers')
        message_saved = await database_sync_to_async(self.sync_database)()
        await communicator.disconnect()
        return self.assertEquals(message_saved.content,'testing consumers')
    def sync_database(self):
        return ChatMessage.objects.get(user=self.user)