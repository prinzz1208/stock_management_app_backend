from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.authentication import generateAccessToken, JWTAuthentication
from users.models import User
from users.serializers import UserSerializer


@api_view(['POST'])
def signup(request):
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException("Passwords do not match!")
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password')

    response = Response()
    token = generateAccessToken(user)
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "jwt": token
    }
    return response


@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'Success'
    }


@api_view(["GET"])
def index(request):
    users = UserSerializer(User.objects.all(),
                           many=True).data  # many = True to tell serializer it is an array of User objects.
    print(users)
    return Response(users)


class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userSerializer = UserSerializer(request.user)
        return Response({
            'data': userSerializer.data
        })
