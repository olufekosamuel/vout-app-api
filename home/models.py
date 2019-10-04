import uuid
from django.db import models
from django.utils import timezone
from users.models import CustomUser

# Create your models here.


CHANNEL_TYPE= (
    ('private', 'private'),
    ('public', 'public'),
)

ROLE_TYPE= (
    ('admin', 'admin'),
    ('super_admin', 'super_admin'),
    ('sub_admin', 'sub_admin'),
    ('user', 'user'),
)

class Channel(models.Model):
    admin = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,unique=True)
    url = models.TextField()
    country = models.CharField(default='',max_length=200)
    state = models.CharField(default='',max_length=200)
    capacity = models.IntegerField(default=1)
    channel_type = models.CharField(default='private', choices=CHANNEL_TYPE, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ChannelInvitation(models.Model):
    Channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class ChannelUsers(models.Model):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    role = models.CharField(default='admin', choices=ROLE_TYPE, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        unique_together = (('channel','user'),)

class ChannelComplain(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    Channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    user = models.ForeignKey(ChannelUsers,on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    is_irrelevant = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ChannelComplainComment(models.Model):
    Complain = models.ForeignKey(ChannelComplain,on_delete=models.CASCADE)
    user = models.ForeignKey(ChannelUsers,on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.description

