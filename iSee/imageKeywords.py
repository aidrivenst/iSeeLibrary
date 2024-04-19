from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
from AppiumLibrary import AppiumLibrary
import base64
from PIL import Image, ImageDraw


class imageKeywords():
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.9'

    def __init__(self, *args):
        self.args = args

    @keyword("Test Keyword")  # the explicit name of the keyword here -- 
    def test_keyword(self, message):
        """Logs a message to the Robot Framework log file."""
        logger.info(message, also_console=True)

    @keyword("Is Image Displayed") 
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
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            image1_tag = f'<img text="Element cherché: " src="data:image/png;base64,{encoded_string}" width="10%">'
            logger.info(" <br> Checking for the presence of the following image <br> " + image1_tag, html=True)   
            #logger.info(f"Checking for the presence of the image at {image_path}")


            #This line use appium image plugin : appium image plugin relay on opencv to capture screenshot in the run time and save to memory only 
            #we are not obliged tu use appium image plugin .. since we are exploring better option than opencv currently 
            #for getting the screenshot in the run we can our plugin later .. 
            #currently we can work with capture page screenshot then do the computer vision part 
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
                with open(image_path, "rb") as image_file:
                    encoded_string2 = base64.b64encode(image_file.read()).decode('utf-8')

                image2_tag = f'<img text="Element cherché: " src="data:image/png;base64,{encoded_string2}" width="10%">'
                logger.info(" <br> Element cible cherché sur la screenshot <br> " + image2_tag, html=True)    
                logger.info(f"Screenshot with highlighted image saved as {modified_screenshot_path}")
            else:
                raise AssertionError(f"Image is not displayed on the screen {modified_screenshot_path}")
        except Exception as e:
            raise AssertionError (f"An error occurred while checking for the image: {str(e)}")
    
    @keyword("Click By Image") 
    def click_by_image(image_path):
        """
        Clicks on an element found by an image using Appium and logs the process.

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
            else:
                raise AssertionError("No element found matching the image.")    
        except Exception as e:
            raise AssertionError(f"An error occurred: {str(e)}")
        


    #     settings = {
    #     'imageMatchThreshold': 0.2,
    #     #'fixImageFindScreenshotDims': True,
    #     #'fixImageTemplateSize': True,
    #     #'checkForImageElementStaleness': True,
    #     #'autoUpdateImageElementPosition': False,
    #     #'imageElementTapStrategy': 'w3cActions'
    # }

    #     # Update settings
    #     driver.update_settings(settings)