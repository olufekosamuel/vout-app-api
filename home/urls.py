from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from .views import *
from rest_framework.routers import DefaultRouter


app_name = "home"

urlpatterns = [
    #path('create/', CreateChannel, name='createchannel'),
    path('verify/',VerifyChannel, name='verify'),
    path('complains/',ComplainList, name='complainList' ),
    path('comments/',ReplyList, name='commentList' ),
    #path('',ListChannelView.as_view(), name='channel' ),
    path('makecomplain/<int:channel_id>/', Complain, name="complain"),
    path('',GetAllChannel,name="getallchannel"),
    path('public/',GetPublicChannel,name="getallpublicchannel"),
    path('info/<int:channel_id>/',GetChannelInfo,name="getchannelinfo"),
    path('comment/<int:complain_id>/',Comment,name="comment"),
]