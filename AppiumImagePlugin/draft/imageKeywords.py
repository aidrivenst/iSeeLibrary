from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
from AppiumLibrary import AppiumLibrary
from appium.webdriver.common.touch_action import TouchAction    
from robot.utils import ConnectionCache
import base64
from PIL import Image, ImageDraw
import io
import cv2
import numpy as np

class imageKeywords():
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.9'

    def __init__(self, *args):
        self.args = args


    @keyword("Is Image Displayed") 
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
    def click_by_image(self, image_path):
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
        
    @keyword("Capture Element Screenshot") 
    def capture_element_screenshot(self, locator):
        """
        Captures a screenshot of a specific element.
        """
        try:
            built_in = BuiltIn()
            appium_lib = built_in.get_library_instance('AppiumLibrary')
            driver = appium_lib._current_application()
            
            element = driver.find_element(AppiumBy.XPATH,locator)
            logger.info(f"element is {element}")
            
            
            # Get the element's location and size
            location = element.location
            size = element.size
            
            logger.info(f"element location {location}")

            driver.save_screenshot("full_screenshot.png")
            import os
            if os.path.exists("full_screenshot.png"):
                logger.info("Screenshot saved.")
            else:
                logger.info("Screenshot not saved.")
                
            image = Image.open("full_screenshot.png")
            
            # bounding box of the element
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            
            # Crop the image to the bounding box
            element_image = image.crop((left, top, right, bottom))

            # Save the cropped image to a bytes buffer
            buffered = io.BytesIO()
            element_image.save(buffered, format="PNG")
            
            # Encode the image to base64
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Save the cropped image
            element_image.save("elementImage.png")

            image1_tag = f'<img text="Element cherché: " src="data:image/png;base64,{img_str}" width="10%">'
            logger.info(" <br> Checking for the presence of the following image <br> " + image1_tag, html=True)  
            return img_str
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            raise ValueError
            

    @keyword("Count Displayed Images")
    def count_displayed_images(self, image_path):
        """
        Counts how many times an image is displayed on the screen using the Appium image plugin.
        
        Args:
            image_path (str): Path to the image file used for finding the element.
        """
        built_in = BuiltIn()
        appium_lib = built_in.get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            image_tag = f'<img src="data:image/png;base64,{encoded_string}" width="10%">'
            logger.info(f"Checking for the presence of the following image:<br>{image_tag}", html=True)

            # Find all elements that match the image
            elements = driver.find_elements(AppiumBy.IMAGE, encoded_string)
            element_count = len(elements)

            driver.save_screenshot('full_screenshot.png')
            screenshot = Image.open('full_screenshot.png')
            draw = ImageDraw.Draw(screenshot)

            # Highlight each found element
            for element in elements:
                location = element.location
                size = element.size
                left = location['x']
                top = location['y']
                right = left + size['width']
                bottom = top + size['height']
                draw.rectangle([left, top, right, bottom], outline="red", width=5)

            # Save the modified screenshot
            modified_screenshot_path = 'highlighted_screenshot.png'
            screenshot.save(modified_screenshot_path)

            logger.info(f"Found {element_count} instances of the image.", html=True)
            logger.info(f"Screenshot with highlighted images saved as {modified_screenshot_path}")

        except Exception as e:
            raise AssertionError(f"An error occurred while checking for the image: {str(e)}")


    @keyword("Click Image Aligned With Text")
    def click_image_aligned_with_text(self, image_path, text):
        """
        Clicks an image (like a toggle) that is aligned horizontally with a given text.
        
        Args:
            image_path (str): The file path to the image to be clicked.
            text (str): The text that the image should be aligned with.
        """
        
        built_in = BuiltIn()
        appium_lib = built_in.get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        locator_text = "//*[@text=\"{}\"]".format(text)
        logger.info(locator_text)
        text_element = driver.find_element(AppiumBy.XPATH,locator_text)
        
        text_location = text_element.location
        text_size = text_element.size
        logger.info(f"text location is : {text_location}")
        logger.info(f"text size is : {text_size}")
        # Assuming the image is horizontally aligned, define the search area:
        y_start = text_location['y']
        #y_end = y_start + text_size['height']
        logger.info(f"text starts at : {y_start}")
        #logger.info(f"text ends at : {y_end}")

        # Step 5: Go through the found images and check alignment with the text element.
        text_center_y = y_start + text_size['height'] / 2
        tolerance = text_size['height'] * 0.5  # 50% tolerance based on text height
        
        logger.info(f"Text center: {text_center_y}, + ou - : {tolerance}")

        # Step 3: Convert the reference image to Base64 for Appium's image recognition.
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        images = driver.find_elements(AppiumBy.IMAGE, base64_image)
        logger.info(f"Found {len(images)} images that match the reference.")
        
        # # Highlight each found element
        # driver.save_screenshot('full_screenshot.png')
        # screenshot = Image.open('full_screenshot.png')
        # draw = ImageDraw.Draw(screenshot)
        # for element in images:
        #     location = element.location
        #     size = element.size
        #     left = location['x']
        #     top = location['y']
        #     right = left + size['width']
        #     bottom = top + size['height']
        #     draw.rectangle([left, top, right, bottom], outline="red", width=5)
        # # Save the modified screenshot
        # modified_screenshot_path = 'Click_image_aligned_with_text.png'
        # screenshot.save(modified_screenshot_path)

        
        # Step 5: Go through the found images and check alignment with the text element.        
        image_found = False
        for img in images:
            img_location = img.location
            img_center_y = img_location['y'] + img.size['height'] / 2
            
            logger.info(f"image center : {img_center_y}")
            logger.info(f"image location : {img_location}")
            # Check if the image is horizontally aligned within the tolerance.
            if text_center_y - tolerance <= img_center_y <= text_center_y + tolerance:
                TouchAction(driver).tap(img).perform()
                logger.info(f"Clicked on image aligned with text '{text}'.")
                image_found = True
                break
            if not image_found:
                error_message = f"No image aligned within tolerance with text '{text}' was found."
                logger.error(error_message)
                raise ValueError(error_message)
            

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
            
    @keyword("Is Image Displayed Using Screenshot")
    def Is_Image_Displayed_Using_Screenshot(self, template_image_path, screenshot_path):

        # Debugging
        print("Image 1 path:", template_image_path)
        print("Image 2 path:", screenshot_path)

        # Charger les images
        image1 = cv2.imread(template_image_path)
        image2 = cv2.imread(screenshot_path)
        if image1 is None or image2 is None:
            raise ValueError("Impossible de charger les images.")
    ###
        result = cv2.matchTemplate(image2, image1, cv2.TM_CCOEFF_NORMED)
        threshold = .85
        locations = np.where(result >= threshold)
        logger.info(locations)
    ####
        # Find the top-left coordinate of the first match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc  # Top-left corner of the matched area
        # Calculate the center of the rectangle to tap
        tap_x = top_left[0] + image1.shape[1] // 2
        tap_y = top_left[1] + image1.shape[0] // 2

        # Log the coordinates to tap on
        logger.info(f"Coordinates to tap: ({tap_x}, {tap_y})")

        with open(template_image_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image1_data = base64.b64encode(image_data).decode('utf-8')
        
        with open(screenshot_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image2_data = base64.b64encode(image_data).decode('utf-8')

        image1_tag = f'<img text="Element cherché: " src="data:image/png;base64,{encoded_image1_data}" width="10%">'
        image2_tag = f'<img src="data:image/png;base64,{encoded_image2_data}" width="10%">'
            # Vérifier s'il y a des correspondances
        if locations[0].size > 0:
            y, x = locations[::-1]
            x, y = x[0], y[0]
            cv2.rectangle(image2, (x, y), (x + image1.shape[1], y + image1.shape[0]), (0, 0, 255), 2)
            
            cv2.imwrite('image2.png', image2)
            
            with open('image2.png', 'rb') as img_file:
                image_data = img_file.read()
                encoded_image_res_data = base64.b64encode(image_data).decode('utf-8')

            with open(template_image_path, 'rb') as img_file:
                image_data = img_file.read()
                encoded_image1_data = base64.b64encode(image_data).decode('utf-8')
            
            with open(screenshot_path, 'rb') as img_file:
                image_data = img_file.read()
                encoded_image2_data = base64.b64encode(image_data).decode('utf-8')
            image_res_tag = f'<img src="data:image/png;base64,{encoded_image_res_data}" width="10%">'

            logger.info(" <br> Element cible cherché sur la screenshot <br> " + image1_tag, html=True)
            logger.info(" <br> Screenshot pris en cours du test <br> "  + image2_tag, html=True)
            logger.info(" <br> Resultat du vérification à l'aide de comparison des images <br> " + image_res_tag, html=True)
        else:
            logger.info('Element not found in devices screen')
            logger.info(" <br> Element cible cherché sur la screenshot <br> " + image1_tag, html=True)
            logger.info(" <br> Screenshot pris en cours du test <br> "  + image2_tag, html=True)
            raise AssertionError ("Element not found in devices screen")

    @keyword("Click Image Using Screenshot")
    def Click_Image_Using_Screenshot(self, template_image_path, screenshot_path):

        # Debugging
        print("Image 1 path:", template_image_path)
        print("Image 2 path:", screenshot_path)

        # Charger les images
        image1 = cv2.imread(template_image_path)
        image2 = cv2.imread(screenshot_path)
        if image1 is None or image2 is None:
            raise ValueError("Impossible de charger les images.")
    ###
        result = cv2.matchTemplate(image2, image1, cv2.TM_CCOEFF_NORMED)
        threshold = .85
        locations = np.where(result >= threshold)
        logger.info(locations)
    ####
        # Find the top-left coordinate of the first match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc  # Top-left corner of the matched area
        # Calculate the center of the rectangle to tap
        tap_x = top_left[0] + image1.shape[1] // 2
        tap_y = top_left[1] + image1.shape[0] // 2

        # Log the coordinates to tap on
        logger.info(f"Coordinates to tap: ({tap_x}, {tap_y})")

        with open(template_image_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image1_data = base64.b64encode(image_data).decode('utf-8')
        
        with open(screenshot_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image2_data = base64.b64encode(image_data).decode('utf-8')

        image1_tag = f'<img text="Element cherché: " src="data:image/png;base64,{encoded_image1_data}" width="10%">'
        image2_tag = f'<img src="data:image/png;base64,{encoded_image2_data}" width="10%">'
            # Vérifier s'il y a des correspondances
        if locations[0].size > 0:
            y, x = locations[::-1]
            x, y = x[0], y[0]
            cv2.rectangle(image2, (x, y), (x + image1.shape[1], y + image1.shape[0]), (0, 0, 255), 2)
            
            cv2.imwrite('image2.png', image2)
            
            with open('image2.png', 'rb') as img_file:
                image_data = img_file.read()
                encoded_image_res_data = base64.b64encode(image_data).decode('utf-8')

            with open(template_image_path, 'rb') as img_file:
                image_data = img_file.read()
                encoded_image1_data = base64.b64encode(image_data).decode('utf-8')
            
            with open(screenshot_path, 'rb') as img_file:
                image_data = img_file.read()
                encoded_image2_data = base64.b64encode(image_data).decode('utf-8')
            image_res_tag = f'<img src="data:image/png;base64,{encoded_image_res_data}" width="10%">'

            logger.info(" <br> Element cible cherché sur la screenshot <br> " + image1_tag, html=True)
            logger.info(" <br> Screenshot pris en cours du test <br> "  + image2_tag, html=True)
            logger.info(" <br> Resultat du vérification à l'aide de comparison des images <br> " + image_res_tag, html=True)
        else:
            logger.info('Element not found in devices screen')
            logger.info(" <br> Element cible cherché sur la screenshot <br> " + image1_tag, html=True)
            logger.info(" <br> Screenshot pris en cours du test <br> "  + image2_tag, html=True)
            raise AssertionError ("Element not found in devices screen")
