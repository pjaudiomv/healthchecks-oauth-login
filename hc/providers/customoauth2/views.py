import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import CustomOAuth2Provider

from hc.settings import (
    CUSTOM_OAUTH2_TOKEN_URL,
    CUSTOM_OAUTH2_AUTHORIZE_URL,
    CUSTOM_OAUTH2_ACCOUNT_URL,
    CUSTOM_OAUTH2_CLIENT_ID,
    CUSTOM_OAUTH2_CLIENT_SECRET
)


class CustomOAuth2Adapter(OAuth2Adapter):
    provider_id = CustomOAuth2Provider.id
    access_token_url = CUSTOM_OAUTH2_TOKEN_URL
    authorize_url = CUSTOM_OAUTH2_AUTHORIZE_URL
    profile_url = CUSTOM_OAUTH2_ACCOUNT_URL
    redirect_uri_protocol = None
    basic_auth = True # XXX specific to KRID ... oof

    def complete_login(self, request, app, token, **kwargs):
        extra_data = requests.get(self.profile_url,headers={
            'Authorization': 'Bearer ' + token.token
        })
        
        return self.get_provider().sociallogin_from_response(
            request,
            extra_data.json()
        )

# re-descend a few classes to use a custom OAuth2View that returns things at runtime.

# override 
class CustomOAuth2LoginView(OAuth2LoginView):
    def get_client(self, request, app):
        # same function
        ret = super(CustomOAuth2LoginView, self).get_client(request, app)
        ret.consumer_key = CUSTOM_OAUTH2_CLIENT_ID
        ret.consumer_secret = CUSTOM_OAUTH2_CLIENT_SECRET
        return ret
class CustomOAuth2CallbackView(OAuth2CallbackView):
    def get_client(self, request, app):
        # same function
        ret = super(CustomOAuth2CallbackView, self).get_client(request, app)
        ret.consumer_key = CUSTOM_OAUTH2_CLIENT_ID
        ret.consumer_secret = CUSTOM_OAUTH2_CLIENT_SECRET
        return ret



oauth2_login = CustomOAuth2LoginView.adapter_view(CustomOAuth2Adapter)
oauth2_callback = CustomOAuth2CallbackView.adapter_view(CustomOAuth2Adapter)
