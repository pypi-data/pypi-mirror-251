import logging

from django.urls import include, path
from duke.common import (
    PluginConfiguration,
    build_plugin,
    build_plugin_manifest_from_package,
)

ENVIRON_PREFIX = "BROWSER_RELOAD"
logger = logging.getLogger(__name__)


class BrowserReloadConfiguration(PluginConfiguration):
    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + [
            "django_browser_reload.middleware.BrowserReloadMiddleware",
        ]

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ["django_browser_reload"]


def plugin():
    name = "django-duke-browser-reload"
    description = "Browser Reload integration for Duke"
    urls = [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

    manifest = build_plugin_manifest_from_package(
        name=name, description=description, urls=urls
    )

    return build_plugin(configuration=BrowserReloadConfiguration, manifest=manifest)
