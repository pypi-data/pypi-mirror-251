"""Provide user configuration constants."""
import sys

from . import config_tools

try:
    config_tools.config_management(["orcid_token"])
except:
    raise ImportError(
        "Please edit your module configuration file %s to define the orcid_token variable."
        % config_tools.config_file()
        + "This token is needed to use orcid's /read-public API."
    )
sys.path.append(config_tools.config_dir())
from scibib_config import orcid_token
