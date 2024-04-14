from robot.api import logger
from robot.api.deco import keyword

class imageKeywords():
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.9'

    def __init__(self, *args):
        self.args = args

    @keyword("Test Keyword")  # the explicit name of the keyword here -- 
    def test_keyword(self, message):
        """Logs a message to the Robot Framework log file."""
        logger.info(message, also_console=True)
