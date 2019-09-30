from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

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

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer

    @csrf_exempt
    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            if serializer.is_valid():
                return JsonResponse({'message': 'logged in','error':False,'status':status.HTTP_200_OK,'data':serializer.data,})
        return Response({'message': 'Wrong credentials','error':True,'status':status.HTTP_401_UNAUTHORIZED})

class LogoutView(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated():
            logout(request)
            return Response({'message': 'Your account has been logged out successfully','error':False,'status':status.HTTP_200_OK})
        else:
            return Response({'message': 'You are not logged in','error':True,'status':status.HTTP_401_UNAUTHORIZED})
    def post(self, request):
        return Response({'message': 'post request not allowed','error':True,'status':status.HTTP_401_UNAUTHORIZED})
