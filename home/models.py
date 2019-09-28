import uuid
from django.db import models
from django.utils import timezone
from users.models import CustomUser

# Create your models here.


CHANNEL_TYPE= (
    (0, 'private'),
    (1, 'public'),
)

ROLE_TYPE= (
    (0, 'admin'),
    (1, 'super_admin'),
    (2, 'sub_admin'),
    (3, 'user'),
)

class Channel(models.Model):
    admin = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    url = models.TextField()
    capacity = models.IntegerField(default=1)
    channel_type = models.PositiveSmallIntegerField(default=1, choices=CHANNEL_TYPE)
    slug = models.SlugField()
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)


    def __str__(self):
        return self.name

class ChannelUsers(models.Model):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(default=1, choices=ROLE_TYPE)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user.email

