"""Djangoflow URL Configuration

Add these to your root URLconf:
    urlpatterns = [
        ...
        path('auth/', include('df_auth.urls'))
    ]

"""
from .viewsets import OTPViewSet
from .viewsets import TokenViewSet
from .viewsets import SignIn, Connect
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("token", TokenViewSet, basename="token")
router.register("otp", OTPViewSet, basename="otp")

urlpatterns = [path("social/", include("social_django.urls", namespace="social"))]
urlpatterns = [path("social/signin/<str:social>/", SignIn.as_view(), name='sign-in')]
urlpatterns = [path("social/connect/<str:social>/", Connect.as_view(), name='connect')]
urlpatterns += router.urls
