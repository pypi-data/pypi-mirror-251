"""widgets for aivatar_project_widgets"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .core import AivProjectWindow

__all__ = ["AivProjectWindow"]

try:
    from pkg_resources import get_distribution
    __version__ = get_distribution(__name__).version
except (Exception, ):
    # Package is not installed
    __version__ = "0.0.0-dev.1"
