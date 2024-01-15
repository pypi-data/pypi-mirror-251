"""Environments handler."""

import tornado
from jupyter_server.base.handlers import APIHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin

from ..._version import __version__


# pylint: disable=W0223
class EnvironmentsHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for the environments."""

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        """Returns the environments."""
        pass
