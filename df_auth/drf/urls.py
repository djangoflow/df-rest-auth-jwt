"""Djangoflow URL Configuration

Add these to your root URLconf:
    urlpatterns = [
        ...
        path('auth/', include('df_auth.urls'))
    ]

"""
from rest_framework.routers import DefaultRouter

from .viewsets import OTPViewSet
from .viewsets import SocialTokenViewSet
from .viewsets import TokenViewSet

router = DefaultRouter()
router.register("token", TokenViewSet, basename="token")
router.register("otp", OTPViewSet, basename="otp")
router.register("social", SocialTokenViewSet, basename="social")

urlpatterns = router.urls