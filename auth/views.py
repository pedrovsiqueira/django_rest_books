from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from utils.utils import validate_password
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token": token.key, "user": serializer.data})

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        password = request.data.get('password')

        if serializer.is_valid():
            if not validate_password(password):
                return Response({
                    "error": (
                        "Password must be at least 8 characters long, "
                        "include at least one uppercase letter, one lowercase letter, "
                        "one number, and one special character."
                    )
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            user = User.objects.get(username=request.data['username'])
            print(user)
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], authentication_classes=[SessionAuthentication, TokenAuthentication],
            permission_classes=[IsAuthenticated])
    def test_token(self, request):
        print(request)
        return Response({"message": f"Token is valid for {request.user.email}"})