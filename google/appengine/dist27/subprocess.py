"""Switch subprocess on and off based on environment variable."""

# pylint: disable=g-import-not-at-top

import os

if os.environ.get("GAE_USE_SUBPROCESS", "1") == "1":
  from python_std_lib import subprocess

  # Can't just do from version.subprocess import * as that skips variables
  # prefixed with an underscore. As this proxy should be transparent, we need
  # every variable.
  globals().update(subprocess.__dict__)
