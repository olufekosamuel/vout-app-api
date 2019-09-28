from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse


@api_view(['POST'])
@csrf_exempt
def CreateChannel(request):

    if request.method == "POST":
        admin = request.user
        name = request.data['name']
        url = request.data['url']
        capacity = 1
        channel_type = request.data['channel_type']
        slug = request.data['slug']

        channel = Channel.objects.create(admin=admin,name=name,url=url,capacity=capacity,channel_type=channel_type,slug=slug)
        channel.save()

        channeluser = ChannelUsers.objects.create(channel=channel,user=request.user,role=1)
        channeluser.save()
        
        return JsonResponse({'message': 'Your channel has been created successfully','error':False,'status':status.HTTP_200_OK})

