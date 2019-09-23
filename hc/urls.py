from django.contrib import admin
from django.conf.urls import include, url
from django.urls import include, path

from hc.accounts import views as accounts_views
from allauth.socialaccount import providers
from importlib import import_module

urlpatterns = [
    path("admin/login/", accounts_views.login),
    path("admin/", admin.site.urls),
    path("accounts/", include("hc.accounts.urls")),
    path("projects/add/", accounts_views.add_project, name="hc-add-project"),
    path(
        "projects/<uuid:code>/settings/",
        accounts_views.project,
        name="hc-project-settings",
    ),
    path(
        "projects/<uuid:code>/remove/",
        accounts_views.remove_project,
        name="hc-remove-project",
    ),
    path("", include("hc.api.urls")),
    path("", include("hc.front.urls")),
    path("", include("hc.payments.urls")),
]

# build allauth provider urls
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns


