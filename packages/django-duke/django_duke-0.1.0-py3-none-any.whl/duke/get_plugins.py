import logging
from importlib.metadata import EntryPoint
from typing import List

from duke.common import Plugin
from duke.conf import DEFAULT_ENTRYPOINT_NAME

logger = logging.getLogger(__name__)


def get_plugins(*, entry_points: List[EntryPoint]) -> List[Plugin]:
    logger.debug("Found %s plugin(s).", len(entry_points))
    raw_plugins = [ep for ep in entry_points if ep.name == DEFAULT_ENTRYPOINT_NAME]
    plugins: List[Plugin] = []
    for raw_plugin in raw_plugins:
        try:
            plugin = raw_plugin.load()
            if plugin is None:
                logger.warning("Plugin %s is not enabled", raw_plugin.name)
                continue
            if not callable(plugin):
                logger.error(
                    "Plugin %s is not a valid plugin. Tip: should be a callable, not %s",
                    plugin,
                    type(plugin),
                )
                continue
            plugin_instance = plugin()
            if not isinstance(plugin_instance, Plugin):
                logger.error(
                    "Plugin %s is not a valid plugin. Tip: should be a Plugin instance, not %s",
                    plugin_instance,
                    type(plugin_instance),
                )
                continue
            plugins.append(plugin_instance)
        except Exception as e:
            # TODO: get rid of catch-all exception
            logger.error("Plugin %s is not a valid plugin", e)
            pass

    return plugins
