from django.conf import settings
from social_core.backends.open_id_connect import OpenIdConnectAuth


class CustomOpenIDConnectAuth(OpenIdConnectAuth):
    name = "oidc"
    OIDC_ENDPOINT = settings.SOCIAL_AUTH_OIDC_ENDPOINT
