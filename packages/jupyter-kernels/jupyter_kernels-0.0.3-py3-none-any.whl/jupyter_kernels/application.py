import sys
import warnings
from pathlib import Path

from datalayer.application import NoStart

from ._version import __version__
from .application_base import JupyterKernelsBaseApp
from .kernel.kernelapp import KernelApp
from .kernel.sessions.sessionsapp import SessionApp
from .kernel.specs.kernelspecsapp import KernelSpecsApp


HERE = Path(__file__).parent


class ConfigExportApp(JupyterKernelsBaseApp):
    """An application to export the configuration."""

    description = """
      An application to export the configuration
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for workspace export.")
            self.exit(1)
        self.log.info("ConfigApp %s", self.version)


class ConfigApp(JupyterKernelsBaseApp):
    """A config app."""

    description = """
    Manage the configuration.
    """

    subcommands = {}
    subcommands["export"] = (
        ConfigExportApp,
        ConfigExportApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error(f"One of `{'`, `'.join(ConfigApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)


class ShellApp(JupyterKernelsBaseApp):
    """A shell application."""

    description = """
      Run predefined scripts.
    """

    def start(self):
        super().start()
        args = sys.argv
        self.log.info(args)


class JupyterKernelsApp(JupyterKernelsBaseApp):
    description = """
      The JupyterKernels application.
    """

    subcommands = {
        "config": (ConfigApp, ConfigApp.description.splitlines()[0]),
        "kernel": (KernelApp, KernelApp.description.splitlines()[0]),
        "kernelspec": (KernelSpecsApp, KernelSpecsApp.description.splitlines()[0]),
        "session": (SessionApp, SessionApp.description.splitlines()[0]),
        "sh": (ShellApp, ShellApp.description.splitlines()[0]),
    }

    def initialize(self, argv=None):
        """Subclass because the ExtensionApp.initialize() method does not take arguments."""
        super().initialize()

    def start(self):
        super(JupyterKernelsApp, self).start()
        self.log.info("JupyterKernels - Version %s - Cloud %s ", self.version, self.cloud)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterKernelsApp.launch_instance

if __name__ == "__main__":
    main()
