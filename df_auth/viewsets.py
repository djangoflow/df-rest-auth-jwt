import logging
from .serializers import OTPObtainSerializer
from .serializers import TokenObtainSerializer
from .serializers import SocialAuthInputSerializer, SocialCallBackSerializer
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.settings import import_string
from rest_framework_simplejwt.settings import api_settings as simple_jwt_settings

from social_core.utils import get_strategy, user_is_authenticated
from social_core.exceptions import AuthException
from social_django.utils import psa, STORAGE
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)

def load_strategy(request=None):
    return get_strategy("df_auth.strategy.DRFStrategy", STORAGE, request)

@psa(settings.REST_SOCIAL_OAUTH_REDIRECT_URI, load_strategy=load_strategy)
def decorate_request(request, backend):
    pass


class ValidationOnlyCreateViewSet(viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(ValidationOnlyCreateViewSet):
    serializer_class = TokenObtainSerializer
    permission_classes = (permissions.AllowAny,)

    @action(
        methods=["post"],
        detail=False,
        serializer_class=import_string(simple_jwt_settings.TOKEN_REFRESH_SERIALIZER),
    )
    def refresh(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(
        methods=["post"],
        detail=False,
        serializer_class=import_string(simple_jwt_settings.TOKEN_VERIFY_SERIALIZER),
    )
    def verify(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(
        methods=["post"],
        detail=False,
        serializer_class=import_string(simple_jwt_settings.TOKEN_BLACKLIST_SERIALIZER),
    )
    def blacklist(self, request, *args, **kwargs):
        if "rest_framework_simplejwt.token_blacklist" not in settings.INSTALLED_APPS:
            raise NotImplementedError

        return self.create(request, *args, **kwargs)


class OTPViewSet(ValidationOnlyCreateViewSet):
    serializer_class = OTPObtainSerializer
    permission_classes = (permissions.AllowAny,)


class SocialAuth(viewsets.GenericViewSet):
    serializer_class = SocialAuthInputSerializer

    def get_object(self):
        user = self.request.user
        self.request.backend.redirect_uri = settings.REST_SOCIAL_OAUTH_REDIRECT
        user = user_is_authenticated(user) and user or None
        self.request.backend.STATE_PARAMETER = False
        user = self.request.backend.complete(user=user)
        return user

    @action(methods=["post"], detail=False)
    def signin(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        decorate_request(request, serializer.validated_data['provider'])
        try:
            user = self.get_object()
        except (AuthException, HTTPError) as e:
            logger.error(e)
            return response.Response("something wrong happened", status.HTTP_400_BAD_REQUEST)
        serializer = TokenObtainSerializer(data={})
        serializer.user = user
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)

    @action(methods=["post"], detail=False, permission_classes=[IsAuthenticated])
    def connect(self, request):
        return self.signin(request)
    
    @action(methods=["get"], detail=False, serializer_class=SocialCallBackSerializer)
    def callback(self, request):
        return response.Response({'code': request.GET['code']})