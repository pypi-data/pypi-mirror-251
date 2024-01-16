import logging
from importlib.metadata import entry_points

from duke.conf import GROUP
from duke.get_plugins import get_plugins
from duke.utils import flatten

logger = logging.getLogger(__name__)


def get_duke_entry_points():
    return entry_points(group=GROUP)


def get_duke_plugins():
    return [ep for ep in get_duke_entry_points() if ep.name == "plugin"]


def get_configuration_class():
    duke_plugins = get_duke_plugins()
    plugins = get_plugins(entry_points=duke_plugins)
    apps_config = tuple([plugin.configuration for plugin in plugins])
    return type("BaseConfig", apps_config, {})


def get_urls():
    duke_plugins = get_duke_plugins()
    plugins = get_plugins(entry_points=duke_plugins)
    urls = flatten(
        [plugin.manifest.urls for plugin in plugins if plugin.manifest.urls is not None]
    )
    logger.debug("Found %s url(s).", len(urls))
    return urls
