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
from django.core import serializers
from rest_framework.exceptions import NotFound
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import exception_handler
from django.http import HttpResponse

def handler404(request, exception):
    raise NotFound(detail="Error 404, page not found", code=404)

def Handler500(request):
    raise NotFound(detail="Error 500, server error", code=500)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status'] = response.status_code
        response.data['error'] = True
        if response.status_code == 401:
            response.data['message'] = response.data['detail']
            del response.data['detail']
        elif response.status_code == 405:
            response.data['message'] = response.data['detail']
            del response.data['detail']

    return response


@api_view(['POST'])
@csrf_exempt
@permission_classes((permissions.IsAuthenticated, ))
def CreateChannel(request):

    if request.method == "POST":
        admin = request.user
        name = request.data.get("channel_name", "")
        url = request.data.get("channel_url", "")
        capacity = 1
        channel_type = request.data.get("channel_type", "")
        if not name or not channel_type or not url:
            return JsonResponse({'message': 'Channel name, type and url is required','error':False,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        try:
            chanel = Channel.objects.get(name__iexact=name)
            return JsonResponse({'message': 'Channel name taken already','error':False,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except Channel.DoesNotExist:
            pass

        if channel_type == 1:
            channel_type = 'private'
        else:
            channel_type = 'public'

        chanel = Channel.objects.create(admin=admin,name=name,url=url,capacity=capacity,channel_type=channel_type)
        chanel.save()

        channeluser = ChannelUsers.objects.create(channel=chanel,user=admin,role='admin')
        channeluser.save()

        data={
            'id': chanel.id,
            'name': chanel.name,
            'url': chanel.url,
        }
        
        return JsonResponse({'message': 'Your channel has been created successfully','data':data,'error':False,'status':status.HTTP_200_OK},status=status.HTTP_200_OK)


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
                return JsonResponse({'message': 'Channel does not exist','error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@csrf_exempt
@permission_classes((permissions.IsAuthenticated, ))
def Complain(request, channel_id):
    if request.method == "POST": 
        pass
    else:
        try:
            chanel = Channel.objects.get(id=channel_id)
            channeluser = ChannelUsers.objects.get(user=request.user,channel=chanel)
        except Channel.DoesNotExist:
            return JsonResponse({'message': 'Channel does not exist','error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except ChannelUsers.DoesNotExist:
            return JsonResponse({'message': 'You dont have access to this channel','error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        complains = ChannelComplain.objects.filter(Channel=chanel).order_by('created_at').first()
        data = ComplainSerializer(complains, many=True)
        return Response({'message': 'Success','error':False,'status':status.HTTP_200_OK, 'data':data.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@csrf_exempt
@permission_classes((permissions.IsAuthenticated, ))
def ComplainList(request):
    if request.method == "GET":
        user = ChannelUsers.objects.filter(user=request.user)

        if not user:
            return JsonResponse({'message': 'You have not joined any channel','error':False,'status':status.HTTP_200_OK, 'data':[]}, status=status.HTTP_200_OK)
        else:
            data = ChannelComplain.objects.filter(user__user__email=request.user.email)
            data = ComplainSerializer(data, many=True)
            return Response({'message': 'Success','error':False,'status':status.HTTP_200_OK, 'data':data.data}, status=status.HTTP_200_OK)
            

@api_view(['GET'])
@csrf_exempt
@permission_classes((permissions.IsAuthenticated, ))
def ReplyList(request):
    if request.method == "GET":
        user = ChannelUsers.objects.filter(user=request.user)

        if not user:
            return JsonResponse({'message': 'You have not joined any channel','error':False,'status':status.HTTP_200_OK, 'data':[]}, status=status.HTTP_200_OK)
        else:
            data = ChannelComplainComment.objects.filter(user__user__email=request.user.email)
            return Response({'message': 'Success','error':False,'status':status.HTTP_200_OK, 'data':data}, status=status.HTTP_200_OK)

class ListChannelView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticated,)