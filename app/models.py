from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    admin = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    name = models.CharField(max_length=200,blank=False,null=False,unique=True)
    slug = models.SlugField(unique=True)
    password = models.CharField(max_length=200,blank=False,null=False)
    created_at =models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    content = models.TextField()
    created_at =models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('created_at',)

class LogedIn(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)