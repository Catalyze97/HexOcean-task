"""
Views for tiers
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissons import UserPermission

from tiers.models import (
    Tier,
    CustomImages,
)
from tiers import serializers


class TierViewSet(viewsets.ModelViewSet):
    """View for manage tiers APIs."""
    serializer_class = serializers.TierDetailSerializer
    queryset = Tier.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def _params_to_ints(self, qs):
        """Converts a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve tiers for authenticated users."""
        queryset = self.queryset
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    # def get_permissions(self):
    #     """Normal users are allowed to get action."""
    #     if self.action == 'post':
    #         self.permission_classes = [IsAdminUser, ]
    #     elif self.action == 'put':
    #         self.permission_classes = [IsAdminUser, ]
    #     elif self.action == 'patch':
    #         self.permission_classes = [IsAdminUser, ]
    #     elif self.action == 'delete':
    #         self.permission_classes = [IsAdminUser, ]
    #     return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TierSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tier."""
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to tiers.',
            )
        ]
    )
)
class CustomImagesViewSet(mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BaseCustomImagesSerializer

    """Manage Custom Images in database."""
    def get_serializer_class(self):
        """Get serializer class belong to tier account. """
        if self.action == 'upload_image':
            return serializers.CustomImagesImageSerializer
        if not self.request.user.account_plan == '':
            if self.request.user.account_plan == 'bp':
                return serializers.BasicCustomImagesSerializer
            elif self.request.user.account_plan == 'pp':
                return serializers.PremiumCustomImagesSerializer
            elif self.request.user.account_plan == 'ep':
                return serializers.EnterpriseCustomImagesSerializer
            else:
                return serializers.AdminCustomImagesSerializer
        else:
            raise ValueError("account_plan for images can't be blank")

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(customimages__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-name').distinct()

    queryset = CustomImages.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to Custom images"""
        custom_img = self.get_object()
        serializer = self.get_serializer(custom_img, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
