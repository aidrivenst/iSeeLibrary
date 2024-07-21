import base64
import os
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from appium.webdriver.common.appiumby import AppiumBy
from locators._locatingstrategy import LocatingStrategy
import robot

class ElementScreenshot(_LoggingKeywords):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.9'
    
    def __init__(self, *args):
        self.args = args

    def encode_image (self, path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
    # @staticmethod
    # def _embed_imagee_to_log(path, width=40):
    #     """Embed an image into the log with an optional custom message."""
    #     logger.info('</td></tr><tr><td colspan="3">'
    #                 f'<img src="data:image/png;base64, {path}" width="{width}%">')



    @keyword("Click On Image")
    def click_On_image(self, path):
        """
        Clicks on an element found by an image using Appium plugin and logs the process.

        Args:
        image_path (str): Path to the image file used for finding the element.

        Returns:
        bool: True if the click was successful, False otherwise.
        """
        built_in = BuiltIn()
        appium_lib = built_in.get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        try:
            encoded_string= self.encode_image(path)
            self._info(f"Attempting to find and click the image at {path}")
            element = driver.find_element(AppiumBy.IMAGE,encoded_string)
            if element:
                nb_element= len(element)
                self._info(f"{nb_element} are found in the current screen")
                element.click()
            else:
                raise AssertionError("No element found matching the image.")
                
        except Exception as e:
            raise AssertionError(f"An error occurred: {str(e)}")