from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from allauth.socialaccount.providers import registry

from allauth.socialaccount.providers.base import AuthAction

from hc.settings import CUSTOM_OAUTH2_DISPLAY_NAME

class CustomOAuth2Account(ProviderAccount):
    pass


class CustomOAuth2Provider(OAuth2Provider):
    id = 'customoauth2'
    name = CUSTOM_OAUTH2_DISPLAY_NAME
    account_class = CustomOAuth2Account
    dummy_app = None

    def extract_uid(self, data):
        return data['username']

    def extract_common_fields(self, data):
        return dict(name=data.get('sub'),
                    email=data.get('username'))

    def get_auth_params(self, request, action):
        ret = super(CustomOAuth2Provider, self).get_auth_params(request, action)
        if action == AuthAction.AUTHENTICATE:
            ret['scope'] = 'user_info'
            # TODO: could use env variables for client id
        return ret
    
    def get_app(self, request=None):
        '''
        Pull client id and secret from settings (in turn pulled from env variables) instead of database.
        Create dummy database object for sake of association to accounts and such, but keep secrets out.
        '''
        from allauth.socialaccount.models import SocialApp # must import this one afterwards for some reason.
        from django.contrib.sites.models import Site

        # create dummy in database if not exist
        site = Site.objects.get_current()
        if not self.dummy_app:
            for provider in registry.get_list():
                if isinstance(provider, CustomOAuth2Provider):
                    try:
                        self.dummy_app = SocialApp.objects.get(provider=provider.id,
                                            sites=site)
                    except SocialApp.DoesNotExist:
                        print ("Installing dummy application credentials for %s."
                            " Real details pulled from settings/env variables." % provider.id)
                        self.dummy_app = SocialApp.objects.create(
                            provider=provider.id,
                            secret='secret',
                            client_id='client-id',
                            name=CUSTOM_OAUTH2_DISPLAY_NAME)
                        self.dummy_app.sites.add(site)
                        self.dummy_app.save()
                    break
        return self.dummy_app

provider_classes = [CustomOAuth2Provider]
