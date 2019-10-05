from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from home.models import Channel, ChannelUsers

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

"""
Registration endpoint, to register a new user on the platform 
and create a new channel after registrations
"""
@api_view(['POST'])
@csrf_exempt
@permission_classes((permissions.AllowAny, ))
def Registration(request):
    fullname = request.data.get("fullname", "")
    password = request.data.get("password", "")
    password2 = request.data.get("password2", "")
    email = request.data.get("email", "")
    country = request.data.get("user_country", "")
    state = request.data.get("user_state", "")
    name = request.data.get("channel_name", "")
    channel_type = request.data.get("channel_type", "")
    url = request.data.get("channel_url", "")
    channel_country = request.data.get("channel_country", "")
    channel_state = request.data.get("channel_state", "")
    capacity = 1

    if not fullname or not password or not email or not password2 or not country or not state:
        return Response(
            {'message': "fullname, email, passwords and location are required to register",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
        )
    elif not name or not channel_type or not url or not channel_country or not channel_state:
        return Response(
            {'message': "channel name, type, url and location are required to register",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        if password != password2:
            return Response(
                {'message': "Those passwords don't match.",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
            )

    try:
        user = CustomUser.objects.get(email=email)
        return Response(
            {'message': "Email has been taken already",'error':True,'status':status.HTTP_401_UNAUTHORIZED},status=status.HTTP_401_UNAUTHORIZED
        )
    except CustomUser.DoesNotExist:
        pass

    try:
        chanel = Channel.objects.get(name__iexact=name)
        return JsonResponse({'message': 'Channel name taken already','error':False,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Channel.DoesNotExist:
        pass
    
    firstname = fullname.split()[0]
    lastname = fullname.split()[1] if len(fullname.split()) > 1 else fullname.split()[0]

    new_user = CustomUser(email=email)
    new_user.set_password(password)
    new_user.first_name = firstname
    new_user.last_name = lastname
    new_user.country = country
    new_user.state = state
    new_user.save()

    if channel_type == 1:
        channel_type = 'private'
    else:
        channel_type = 'public'
    
    channel = Channel.objects.create(admin=new_user,name=name,url=url,capacity=capacity,channel_type=channel_type,country=country,state=state)
    channel.save()

    channeluser = ChannelUsers.objects.create(channel=channel,user=new_user,role='admin')
    channeluser.save()

    data = {
        'id': new_user.id,
        'full name': fullname,
        'email': new_user.email,
        'channel_name': channel.name,
    }

    return Response({'message': 'Your account and channel has been created successfully','error':False,'status':status.HTTP_201_CREATED,'data':data,})


"""
Get user info endpoint, to get informations about an authenticated user
"""
@api_view(['GET'])
@csrf_exempt
@permission_classes((permissions.IsAuthenticated, ))
def GetUserInfo(request):
    user = CustomUser.objects.get(email=request.user.email)
    data = {
        'id': user.id,
        'fullname': user.first_name+" "+user.last_name,
        'email': user.email,
        'state': user.state,
        'country': user.country
    }
    return Response({'message': 'success','error':False,'status':status.HTTP_201_CREATED,'data':data,})


@api_view(['POST'])
@csrf_exempt
@permission_classes((permissions.AllowAny, ))
def RegistrationForExistingChannel(request):
    pass


"""
@api_view(['POST'])
@csrf_exempt
@permission_classes((permissions.AllowAny, ))
def RegistrationForExistingChannel(request):
    if request.method == "POST":
        fullname = request.data.get("fullname", "")
        password = request.data.get("password", "")
        password2 = request.data.get("password2", "")
        country = request.data.get("country", "")
        state = request.data.get("state", "")
        email = request.data.get("email", "")
        url = request.data.get("channel_url", "")

        if not fullname or not password or not email or not password2 or not url or not country or not state:
            return Response(
                {'message': "fullname, email, passwords are required to register",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if password != password2:
                return Response(
                    {'message': "Those passwords don't match.",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
                )

        try:
            user = CustomUser.objects.get(email=email)
            return Response(
                {'message': "Email has been taken already",'error':True,'status':status.HTTP_401_UNAUTHORIZED},status=status.HTTP_401_UNAUTHORIZED
            )
        except CustomUser.DoesNotExist:
            pass
        
        new_user = CustomUser.objects.create_user(
            username=username, password=password, email=email
        )
        
        channel = Channel.objects.get(url=url)

        channeluser = ChannelUsers.objects.create(channel=channel,user=new_user,role='user')
        channeluser.save()
        channel.capacity += 1
        channel.save()

        data = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'channel_name': channel.name,
        }

        return Response({'message': 'Your account has been created and you have joined the channel successfully','error':False,'status':status.HTTP_201_CREATED,'data':data,})
"""
class UserListView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        password2 = request.data.get("password2", "")
        email = request.data.get("email", "")

        if not username or not password or not email or not password2:
            return Response(
                {'message': "username, email and passwords are required to register",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if password != password2:
                return Response(
                    {'message': "Those passwords don't match.",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
                )

        try:
            user = CustomUser.objects.get(username=username)
            return Response(
                {'message': "Username has been taken already",'error':True,'status':status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED
            )
        except CustomUser.DoesNotExist:
            pass

        try:
            user = CustomUser.objects.get(email=email)
            return Response(
                {'message': "Username has been taken already",'error':True,'status':status.HTTP_401_UNAUTHORIZED},status=status.HTTP_401_UNAUTHORIZED
            )
        except CustomUser.DoesNotExist:
            pass
        
        new_user = CustomUser.objects.create_user(
            username=username, password=password, email=email
        )

        data = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }
        return Response({'message': 'Your account has been created successfully','error':False,'status':status.HTTP_201_CREATED,'data':data,})


"""
Login endpoint, to authenticate a user and provide a jwt for the user
"""
class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        
        if not email or not password:
            return Response(
                {'message': "email and password are required to login",'error':True,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            if serializer.is_valid():
                return JsonResponse({'message': 'logged in','error':False,'status':status.HTTP_200_OK,'data':serializer.data,})
        return Response({'message': 'Wrong credentials','error':True,'status':status.HTTP_401_UNAUTHORIZED})
