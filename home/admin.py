from django.contrib import admin

# Register your models here.
from .models import Channel, ChannelUsers, ChannelComplain, ChannelComplainComment, ChannelInvitation

admin.site.register(Channel) 
admin.site.register(ChannelUsers)
admin.site.register(ChannelComplain)
admin.site.register(ChannelComplainComment)
admin.site.register(ChannelInvitation)