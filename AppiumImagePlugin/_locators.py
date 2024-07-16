from appium.webdriver.common.appiumby import MobileBy
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class ImageLocator:
    def __init__(self):
        self.driver = BuiltIn().get_library_instance('AppiumLibrary')._current_application()

    def _element_at_coordinates(self, coordinates):

        x, y = coordinates
        return self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                        f'new UiSelector().descriptionContains("{x},{y}")')



    def _load_templates(self):
        templates = {
            'bus': 'path/to/Bus.png',
            'covoitici': 'path/to/Covoitici.png',
            'covoiturage': 'path/to/Covoiturage.png',
            'cristolib': 'path/to/Cristolib.png',
        }
        return templates

    @keyword
    def click_ai_image(self, element_name):
        image_path = self.templates.get(element_name)
        if not image_path:
            self._warn(f"Template for {element_name} not found.")
            raise Exception(f"Template for {element_name} not found.")
        coordinates = self._find_element_by_image(image_path)
        self.driver.tap([coordinates])
        self._info(f"Clicked on element {element_name} at {coordinates}")

    @keyword
    def is_ai_image_displayed(self, element_name):
        image_path = self.templates.get(element_name)
        if not image_path:
            self._war(f"Template for {element_name} not found.")
            raise Exception(f"Template for {element_name} not found.")
        try:
            self._find_element_by_image(image_path)
            self._info(f"Element {element_name} is displayed.")
            return True
        except Exception:
            self._info(f"Element {element_name} is not displayed.")
            return False

    def _find_element_by_image(self, image_path):
        screenshot = self._get_screenshot()
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8
        if max_val >= threshold:
            top_left = max_loc
            h, w = template.shape
            center = (top_left[0] + w // 2, top_left[1] + h // 2)
            self._debug(f"Element found at {center} with confidence {max_val}")
            return center
        else:
            self._warn(f"Element with image {image_path} not found on screen.")
            raise Exception(f"Element with image {image_path} not found on screen.")

