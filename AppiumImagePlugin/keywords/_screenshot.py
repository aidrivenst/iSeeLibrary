from robot.api.deco import keyword, not_keyword
import os
import robot
import base64
from keywordgroup import KeywordGroup
from AppiumImagePlugin.locators import ElementFinder
from ._logging import _LoggingKeywords
class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()
        self._logging = _LoggingKeywords()
    @not_keyword
    def capture_page_screenshot_base64(self):
        driver = self._current_application()
        screenshot_base64 = driver.get_screenshot_as_base64()
        return screenshot_base64
    
    @keyword
    def capture_element_screenshot(self,locator, screenshot_name=None):
        """ capture element screenshot using locator
        default name : element-screenshot
        this function do not log the image
        """
        element = self._element_finder._element_find(locator, True, True)
        
        if screenshot_name:
            path, link = self._get_screenshot_paths(screenshot_name)

            if hasattr(self._current_application(), 'get_screenshot_as_file'):
                element.get_screenshot_as_file(path)
            else:
                element.save_screenshot(path)

            self._logging._log_image()
            return path
        else:
            base64_screenshot = element.get_screenshot_as_base64()
            self._html('</td></tr><tr><td colspan="3">'
                       '<img src="data:image/png;base64, %s" width="800px">' % base64_screenshot)
            return None

    #private
    def _image_to_base64(self,image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file does not exist: {image_path}")
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            return encoded_image

    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            filename = 'screenshot-%d.png' % self._screenshot_index
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link