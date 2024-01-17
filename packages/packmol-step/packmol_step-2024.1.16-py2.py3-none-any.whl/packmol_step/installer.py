# -*- coding: utf-8 -*-

"""Installer for the PACKMOL plug-in.

This handles any further installation needed after installing the Python
package `packmol-step`.
"""

import logging
from pathlib import Path
import pkg_resources
import subprocess

import seamm_installer

logger = logging.getLogger(__name__)


class Installer(seamm_installer.InstallerBase):
    """Handle further installation needed after installing packmol-step.

    The Python package `packmol-step` should already be installed, using `pip`,
    `conda`, or similar. This plug-in-specific installer then checks for the
    PACKMOL executable, installing it if needed, and registers its
    location in seamm.ini.

    There are a number of ways to determine which are the correct PACKMOL
    executables to use. The aim of this installer is to help the user locate
    the executables. There are a number of possibilities

    1.  The correct executables are already available.

        1. If they are already registered in `seamm.ini` there is nothing else
           to do.
        #. They may be in the current path, in which case they need to be added
           to `seamm.ini`.
        #. If a module system is in use, a module may need to be loaded to give
           access to PACKMOL.
        #. They cannot be found automatically, so the user needs to locate the
           executables for the installer.

    #.  PACKMOL is not installed on the machine. In this case they can be
        installed in a Conda environment. There is one choice

        1. They can be installed in a separate environment, `seamm-packmol` by
           default.
    """

    def __init__(self, logger=logger):
        # Call the base class initialization, which sets up the commandline
        # parser, amongst other things.
        super().__init__(logger=logger)

        logger.debug("Initializing the PACKMOL installer object.")

        self.section = "packmol-step"
        self.path_name = "packmol-path"
        self.executables = ["packmol"]
        self.resource_path = Path(pkg_resources.resource_filename(__name__, "data/"))
        # What Conda environment is the default?
        data = self.configuration.get_values(self.section)
        if "conda-environment" in data and data["conda-environment"] != "":
            self.environment = data["conda-environment"]
        else:
            self.environment = "seamm-packmol"

        # The environment.yaml file for Conda installations.
        path = Path(pkg_resources.resource_filename(__name__, "data/"))
        logger.debug(f"data directory: {path}")
        self.environment_file = path / "seamm-packmol.yml"

    def exe_version(self, path):
        """Get the version of the PACKMOL executable.

        Parameters
        ----------
        path : pathlib.Path
            Path to the executable.

        Returns
        -------
        str
            The version reported by the executable, or 'unknown'.
        """
        try:
            result = subprocess.run(
                [str(path), "-log", "none"],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
            )
        except Exception:
            version = "unknown"
        else:
            version = "unknown"
            lines = result.stdout.splitlines()
            for line in lines:
                line = line.strip()
                tmp = line.split()
                if len(tmp) == 2:
                    key, value = tmp
                    if key == "Version":
                        version = value
                        break

        return version
