from io import BytesIO
import io
from PIL import Image
import base64
from robot.api import logger
from appium.webdriver.common.appiumby import AppiumBy
from robot.libraries.BuiltIn import BuiltIn
from PIL import Image, ImageDraw
import os
import cv2
from imageLogger import embed_image_to_log


def is_image_displayed(image_path):
    """
    Checks if an image is displayed on the screen using OpenCV.
    
    Args:
        image_path (str): Path to the image file used for finding the element.
    
    """

    built_in = BuiltIn()
    appium_lib = built_in.get_library_instance('AppiumLibrary')
    driver = appium_lib._current_application()
    
    try:
        embed_image_to_log(image_path, "Checking for the presence of the following image")
        
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
            
            embed_image_to_log(modified_screenshot_path, "Image has been found in the currrent screen")

            #logger.info(f"Screenshot with highlighted image saved as {modified_screenshot_path}")
        else:
            raise AssertionError(f"Image is not displayed on the screen {modified_screenshot_path}")
    except Exception as e:
        raise AssertionError (f"An error occurred while checking for the image: {str(e)}")