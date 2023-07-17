"""Import tktermwidget package"""
import utils

utils.check()  # Check the files

# Import them after the check
from .style import *  # noqa: F401, F403, E402
from .widgets import Terminal  # noqa: F401, E402
