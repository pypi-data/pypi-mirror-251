"""The Jupyter Content Server application."""

import os

from traitlets import Unicode

from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin

from ._version import __version__

from .handlers.index.handler import IndexHandler
from .handlers.config.handler import ConfigHandler
from .handlers.content.handler import ContentHandler
from .handlers.echo.handler import WsEchoHandler
from .handlers.relay.handler import WsRelayHandler
from .handlers.proxy.handler import WsProxyHandler
from .handlers.ping.handler import WsPingHandler


DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "./static")

DEFAULT_TEMPLATE_FILES_PATH = os.path.join(os.path.dirname(__file__), "./templates")


class JupyterContentExtensionApp(ExtensionAppJinjaMixin, ExtensionApp):
    """The Jupyter Content Server extension."""

    name = "jupyter_content"

    extension_url = "/jupyter_content"

    load_other_extensions = True

    static_paths = [DEFAULT_STATIC_FILES_PATH]
    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]

    config_a = Unicode("", config=True, help="Config A example.")
    config_b = Unicode("", config=True, help="Config B example.")
    config_c = Unicode("", config=True, help="Config C example.")

    def initialize_settings(self):
        self.log.debug("Jupyter Content Config {}".format(self.config))

    def initialize_templates(self):
        self.serverapp.jinja_template_vars.update({"jupyter_content_version" : __version__})

    def initialize_handlers(self):
        self.log.debug("Jupyter Content Config {}".format(self.settings['jupyter_content_jinja2_env']))
        handlers = [
            ("jupyter_content", IndexHandler),
            (url_path_join("jupyter_content", "config"), ConfigHandler),
            (url_path_join("jupyter_content", "content"), ContentHandler),
            (url_path_join("jupyter_content", "echo"), WsEchoHandler),
            (url_path_join("jupyter_content", "relay"), WsRelayHandler),
            (url_path_join("jupyter_content", "proxy"), WsProxyHandler),
            (url_path_join("jupyter_content", "ping"), WsPingHandler),
        ]
        self.handlers.extend(handlers)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterContentExtensionApp.launch_instance
