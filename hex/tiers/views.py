"""
Views for tiers
"""

from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Converts a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve tiers for authenticated users."""
        queryset = self.queryset
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TierSerializer
    #     elif self.action == 'upload_image':
    #         return serializers.TierImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tier."""
        serializer.save(user=self.request.user)


class CustomImagesViewSet(mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = serializers.BaseCustomImagesSerializer
    """Manage Custom Images in database."""
    def get_serializer_class(self):
        """Get serializer class belong to tier account. """
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

    queryset = CustomImages.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')



    # @action(methods=['POST'], detail=True, url_path='upload-image')
    # def upload_image(self, request, pk=None):
    #     """Upload an image to tier"""
    #     tier = self.get_object()
    #     serializer = self.get_serializer(tier, data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
