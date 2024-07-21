import base64
import io
from io import BytesIO
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
from PIL import Image, ImageDraw
from robot.api.deco import keyword
import os


@keyword
def is_image_displayed(image_path):
    """
    Checks if an image is displayed on the screen using image plugin.
    
    Args:
        image_path (str): Path to the image file used for finding the element.
    
    """

    built_in = BuiltIn()
    appium_lib = built_in.get_library_instance('AppiumLibrary')
    driver = appium_lib._current_application()
    
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        image1_tag = f'<img text="Element cherché: " src="data:image/png;base64,{encoded_string}" width="10%">'
        logger.info(" <br> Checking for the presence of the following image <br> " + image1_tag, html=True)   
        #logger.info(f"Checking for the presence of the image at {image_path}")

        element = driver.find_element(AppiumBy.IMAGE, encoded_string)
        logger.info(f"Element has been found by appium : {element}")   


        driver.save_screenshot('full_screenshot.png')
 
        if element:
            logger.info("Image is displayed on the screen.")

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
            with open(image_path, "rb") as image_file:
                encoded_string2 = base64.b64encode(image_file.read()).decode('utf-8')

            image2_tag = f'<img text="Element cherché: " src="data:image/png;base64,{encoded_string2}" width="10%">'
            logger.info(" <br> Element cible cherché sur la screenshot <br> " + image2_tag, html=True)    
            logger.info(f"Screenshot with highlighted image saved as {modified_screenshot_path}")
        else:
            raise AssertionError(f"Image is not displayed on the screen {modified_screenshot_path}")
    except Exception as e:
        raise AssertionError (f"An error occurred while checking for the image: {str(e)}")
