import base64
import os
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from appium.webdriver.common.appiumby import AppiumBy
from locators._locatingstrategy import LocatingStrategy
import robot
from AppiumImage.__logging import _LoggingKeywords

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

    @keyword("Take Element Screenshot")
    def get_appium_element_screenshot(self, locator, filename=None):
        """Capture element screenshot using Appium.
        Default filename: 'appiumelementscreenshot.png'
        This function does not log the image.
        """
        built_in = BuiltIn()
        appium_lib = built_in.get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()
        element = driver.find_element(AppiumBy.XPATH, locator)
        logger.info(f'{element}')
        if filename:
            path, link = self._get_screenshot_paths(filename)
            logger.info(f'{path}')
            if hasattr(driver, 'get_screenshot_as_file'):
                element.screenshot(path)
            else:
                element.save_screenshot(path)
            self._embed_image_to_log(link, 40)
            return path
        else:
            base64_screenshot = element.get_screenshot_as_base64()
            self._embed_image_to_log(base64_screenshot, 40)
            return None

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



    def is_image_displayed(self, image_path):
        """
        Checks if an image is displayed on the screen using OpenCV.
        
        Args:
            image_path (str): Path to the image file used for finding the element.
        
        """

        built_in = BuiltIn()
        appium_lib = built_in.get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()
        
        try:
            self._embed_image_to_log(image_path)
            
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            element = driver.find_element(AppiumBy.IMAGE, encoded_string)

            driver.save_screenshot('full_screenshot.png')

            if element:
                logger.info("Image is displayed on the screen.")

                # Take a screenshot of the entire screen
                screenshot = Image.open('full_screenshot.png')
                draw = ImageDraw.Draw(screenshot)            
                location = element.location
                size = element.size

                left = location['x']
                top = location['y']
                right = left + size['width']
                bottom = top + size['height']
                
                draw.rectangle([left, top, right, bottom], outline="red", width=5)
                
                # Save screenshot == a revoir
                modified_screenshot_path = 'highlighted_screenshot.png'
                screenshot.save(modified_screenshot_path)
                
                self.embed_image_to_log(modified_screenshot_path, "Image has been found in the currrent screen")

                #logger.info(f"Screenshot with highlighted image saved as {modified_screenshot_path}")
            else:
                raise AssertionError(f"Image is not displayed on the screen {modified_screenshot_path}")
        except Exception as e:
            raise AssertionError (f"An error occurred while checking for the image: {str(e)}")



    #@staticmethod
    def _get_screenshot_paths(self, filename):
        filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link