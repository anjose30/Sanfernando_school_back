from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomUserSerializer, EmailTokenObtainPairSerializer


class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
