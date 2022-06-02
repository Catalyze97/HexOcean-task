"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.serializers import (
    BaseUserSerializer,
    UserSerializer,
    AuthTokenSerializer,
    AdminUserSerializer,
    NormalUserSerializer,

)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    serializers = {
        AdminUserSerializer,
        NormalUserSerializer,
        UserSerializer,
    }

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminUserSerializer
        # if self.request.user.account_plan == 'bp':
        #     print(self.request.user.account_plan)
        #     return AdminUserSerializer
        if not self.request.user.is_staff:
            return NormalUserSerializer
        # else:
        #     print(self.request.user.account_plan)



    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


