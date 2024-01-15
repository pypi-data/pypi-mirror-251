import warnings

from datalayer.application import NoStart

from ...application_base import JupyterpoolBaseApp


class PoolListApp(JupyterpoolBaseApp):
    """An application to list the kernels."""

    description = """
      An application to list the kernels.
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for kernel list.")
            self.exit(1)
        self.log.info("PoolListApp %s %s %s", self.base_url, self.base_ws_url, self.version)


class PoolApp(JupyterpoolBaseApp):
    """A Pool application."""

    description = """
      The Jupyterpool application for Pools.
    """

    subcommands = {}
    subcommands["list"] = (
        PoolListApp,
        PoolListApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error(f"One of `{'`, `'.join(PoolApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)
