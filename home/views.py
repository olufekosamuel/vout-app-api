from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.exceptions import NotFound
from rest_framework.authentication import TokenAuthentication

def handler404(request, exception):
    raise NotFound(detail="Error 404, page not found", code=404)

def Handler500(request):
    raise NotFound(detail="Error 500, server error", code=500)


@api_view(['POST'])
@csrf_exempt
def CreateChannel(request):

    if request.method == "POST":
        admin = request.user
        name = request.data.get("name", "")
        url = request.data.get("url", "")
        capacity = 1
        channel_type = request.data.get("channel_type", "")
        slug = request.data.get("slug", "")

        channel = Channel.objects.create(admin=admin,name=name,url=url,capacity=capacity,channel_type=channel_type,slug=slug)
        channel.save()

        channeluser = ChannelUsers.objects.create(channel=channel,user=request.user,role=1)
        channeluser.save()
        
        
        return JsonResponse({'message': 'Your channel has been created successfully','error':False,'status':status.HTTP_200_OK})

@api_view(['POST'])
@csrf_exempt
@permission_classes((permissions.AllowAny, ))
def VerifyChannel(request):
    if request.method == "POST":
        name = request.data.get("name", "")

        if not name:
            return JsonResponse({'message': 'Channel name cannot be empty','error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                chanel = Channel.objects.get(name__iexact=name)
                return JsonResponse({'message': 'Channel exist','error':False,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            except Channel.DoesNotExist:
                return JsonResponse({'message': 'Channel does not exist','error':True,'status':status.HTTP_400_BAD_REQUEST})

class ListChannelView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticated,)