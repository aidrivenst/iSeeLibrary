from appium.webdriver.common.appiumby import AppiumBy

class LocatingStrategy:
    @staticmethod
    def locating_strategy(locator : str):
        """
        Determines if the locator is an XPath or an ID.

        Args:
        locator (str): The locator string to evaluate.

        Returns:
        str: 'xpath' if the locator is an XPath expression, otherwise 'id'.
        """
        if locator.startswith('/') or locator.startswith('('):
            return AppiumBy.XPATH
        else:
            return AppiumBy.ID
