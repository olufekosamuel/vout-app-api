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
    name = models.CharField(max_length=200)
    url = models.TextField()
    capacity = models.IntegerField(default=1)
    channel_type = models.CharField(default='private', choices=CHANNEL_TYPE, max_length=200)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)


    def __str__(self):
        return self.name

class ChannelUsers(models.Model):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    role = models.CharField(default='admin', choices=ROLE_TYPE, max_length=200)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user.email

