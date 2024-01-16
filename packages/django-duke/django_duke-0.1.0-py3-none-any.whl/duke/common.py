from dataclasses import dataclass
from typing import List, Optional, Type, Union

import pkg_resources
from django.urls import URLPattern
from django.urls.resolvers import URLResolver


class PluginConfiguration:
    """
    Duck-typed class for plugin configuration.
    See https://django-configurations.readthedocs.io/en/stable/values.html#overview
    """

    MIDDLEWARE: List[str] = []
    INSTALLED_APPS: List[str] = []

    @classmethod
    def pre_setup(cls):
        ...

    @classmethod
    def post_setup(cls):
        ...


@dataclass
class PluginManifest:
    name: str
    description: str
    version: str
    urls: Optional[List[Union[URLPattern, URLResolver]]] = None


@dataclass
class Plugin:
    configuration: Type[PluginConfiguration]
    manifest: PluginManifest


def build_plugin_manifest_from_package(
    *, name, description, urls: Optional[List[Union[URLPattern, URLResolver]]] = None
):
    pkg = pkg_resources.get_distribution(name)
    return PluginManifest(name, description, pkg.version, urls)


def build_plugin(*, configuration: Type[PluginConfiguration], manifest: PluginManifest):
    return Plugin(configuration, manifest)
