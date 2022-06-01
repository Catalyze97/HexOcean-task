"""
URL mappings for the tiers app.
"""

from django.urls import(
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('tiers', views.TierViewSet)

app_name = 'tiers'

urlpatterns = [
    path('', include(router.urls)),

]
