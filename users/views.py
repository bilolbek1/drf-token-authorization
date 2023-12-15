from rest_framework.authtoken.models import Token
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout
from users.models import CustomUser
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # user = CustomUser.objects.get(username=request.data['username'])
            # access_token = Token.objects.get(user=user)

            # serializer = UserSerializer(user)

            data = {
                'user': serializer.data,
                # 'access_token': access_token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            get_user = CustomUser.objects.get(username=request.data['username'])
            serializer = UserSerializer(get_user)

            token = Token.objects.create(user=get_user)

            # if access_token:
            #     data['access_token'] = access_token.key
            # elif create_token:
            #     data['access_token'] = create_token.key

            data = {
                'user': serializer.data,
                'token': token.key,
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response({'message': "User not found"}, status=status.HTTP_400_BAD_REQUEST)





class TestAPIView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = {
            'message': 'That is Test Page'
        }
        return Response(data)



class LogoutAPIView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'You have successfully logged out'})