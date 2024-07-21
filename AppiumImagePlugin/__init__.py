from AppiumImagePlugin.keywords import *
from AppiumImagePlugin.version import VERSION

__version__ = VERSION


class AppiumLibrary(
    _LoggingKeywords,
    _ScreenshotKeywords,
    ImageKeywords
):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION