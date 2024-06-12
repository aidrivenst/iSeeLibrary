import os
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from appium.webdriver.common.appiumby import AppiumBy
from locators._locatingstrategy import LocatingStrategy
import robot

class ElementScreenshot:
    
    @staticmethod
    def _embed_image_to_log(path, width=40):
        """Embed an image into the log with an optional custom message."""
        logger.info('</td></tr><tr><td colspan="3">'
                    f'<img src="data:image/png;base64, {path}" width="{width}%">')

    @keyword
    def get_appium_element_screenshot(self, locator, filename=None):
        """Capture element screenshot using Appium.
        Default filename: 'appiumelementscreenshot.png'
        This function does not log the image.
        """
        built_in = BuiltIn()
        appium_lib = built_in.get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()
        element = driver.find_element(LocatingStrategy(locator), locator)
        
        if filename:
            path, link = self._get_screenshot_paths(filename, driver)

            if hasattr(driver, 'get_screenshot_as_file'):
                element.get_screenshot_as_file(path)
            else:
                element.save_screenshot(path)
            self._embed_image_to_log(link, 40)
            return path
        else:
            base64_screenshot = element.get_screenshot_as_base64()
            self._embed_image_to_log(base64_screenshot, 40)
            return None

    @staticmethod
    def _get_screenshot_paths(filename):
        filename = filename.replace('/', os.sep)
        logdir = ElementScreenshot._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    @staticmethod
    def _get_log_dir():
        logdir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        return logdir
