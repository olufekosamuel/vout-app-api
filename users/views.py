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

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserListView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        data = serializer.data
        headers = self.get_success_headers(serializer.data)

        return Response({'message': 'Your account has been created successfully','error':False,'status':status.HTTP_200_OK,'data':data,})

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
        logout(request)
        return Response({'message': 'Your account has been logged out successfully','error':False,'status':status.HTTP_200_OK})
