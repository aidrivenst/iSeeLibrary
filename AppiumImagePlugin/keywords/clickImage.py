import base64
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
from robot.api.deco import *

class clickImage():

    def __init__(self, *args):
        #self.image_path = image_path
        self.args = args


    @keyword("Click On Image")
    def click_On_image(self, image_path):
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
            # mandatory to convert it : it works like this :/ ---- WIP to implement training on our picto 
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            logger.info(f"Attempting to find and click the image at {image_path}")
            
            # use appiumBy +  encoded string 
            element = driver.find_element(AppiumBy.IMAGE,encoded_string)
            logger.info (element)
            if element:
                element.click()
                logger.info("Click successful.")
                return True
            else:
                raise AssertionError("No element found matching the image.")
                
        except Exception as e:
            raise AssertionError(f"An error occurred: {str(e)}")

    @keyword("Auto Scaler Image Clicker")
    def auto_scaler_image_clicker(self, image_path):
        """
        Automatically scales the image until it finds the element.

        Args:
        image_path (str): Path to the image file used for finding the element.
        """
        built_in = BuiltIn()
        appium_lib = built_in.get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        scale = 1.0
        found = False

        while not found and scale > 0:
            scaled_image_path = scale_appium_image_single_factor(image_path, scale)
            
            with open(scaled_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            try:
                element = driver.find_element(AppiumBy.IMAGE, encoded_string)
                elements = driver.find_elements(AppiumBy.IMAGE, encoded_string)
                logger.info (f" elements found {elements}")
                logger.info (f" length of elements {len(elements)}")
                if element:
                    logger.info(f"Element found {element}")
                    location = element.location
                    logger.info(f"Element location: x = {location['x']}, y = {location['y']}")
                    
                    element.click()
                    logger.info(f"Element found and clicked at scale {scale}")
                    found = True
                    exit
                else:
                    logger.info(f"Element not found at scale {scale}, trying smaller scale.")
            except Exception as e:
                logger.info(f"Exception occurred at scale {scale}: {e}")
                logger.info(f"Element not found at scale {scale}, trying smaller scale.")

            scale -= 0.1

        if not found:
            raise AssertionError("Element has not been found at any scale.")