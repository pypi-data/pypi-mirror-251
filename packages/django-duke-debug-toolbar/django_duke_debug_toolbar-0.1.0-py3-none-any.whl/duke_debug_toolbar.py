import logging

from configurations import values
from django.urls import include, path
from duke.common import (
    PluginConfiguration,
    build_plugin,
    build_plugin_manifest_from_package,
)

ENVIRON_PREFIX = "DEBUG_TOOLBAR"
logger = logging.getLogger(__name__)


class DebugToolbarConfiguration(PluginConfiguration):
    INTERNAL_IPS = values.ListValue(
        environ_prefix=ENVIRON_PREFIX, default=["127.0.0.1"]
    )

    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ["debug_toolbar"]


def plugin():
    name = "django-duke-debug-toolbar"
    description = "Debug Toolbar integration for Duke"
    urls = [path("__debug__/", include("debug_toolbar.urls"))]

    manifest = build_plugin_manifest_from_package(
        name=name, description=description, urls=urls
    )

    return build_plugin(configuration=DebugToolbarConfiguration, manifest=manifest)
