from typing import List

from django.conf import settings
from rest_framework.settings import APISettings

DEFAULTS = {
    "USER_CREATE_REQUIRED_FIELDS": {
        "email": "rest_framework.serializers.EmailField",
    },
    "USER_CREATE_OPTIONAL_FIELDS": {
        "first_name": "rest_framework.serializers.CharField",
        "last_name": "rest_framework.serializers.CharField",
        "password": "rest_framework.serializers.CharField",
        "phone_number": "phonenumber_field.serializerfields.PhoneNumberField",
    },
    "USER_IDENTITY_FIELDS": {
        "username": "rest_framework.serializers.CharField",
        "email": "rest_framework.serializers.CharField",
        "phone_number": "phonenumber_field.serializerfields.PhoneNumberField",
    },
    "REQUIRED_AUTH_FIELDS": {},
    "OPTIONAL_AUTH_FIELDS": {
        "otp": "rest_framework.serializers.CharField",
        "password": "rest_framework.serializers.CharField",
    },
    "TEST_USER_EMAIL": None,
    "OTP_IDENTITY_UPDATE_FIELD": True,
    "OTP_DEVICE_MODELS": {
        "email": "django_otp.plugins.otp_email.models.EmailDevice",
        "totp": "django_otp.plugins.otp_totp.models.TOTPDevice",
        "sms": "otp_twilio.models.TwilioSMSDevice",
    },
    "OTP_AUTO_CREATE_ACCOUNT": True,
    "SEND_OTP_UNAUTHORIZED_USER": True,
    "SIGNUP_ALLOWED": True,
}

IMPORT_STRINGS: List[str] = []

api_settings = APISettings(getattr(settings, "DF_AUTH", IMPORT_STRINGS), DEFAULTS)
