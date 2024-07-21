from AppiumLibrary import utils
from appium.webdriver.common.appiumby import AppiumBy
from robot.api import logger
import ast
from unicodedata import normalize
from selenium.webdriver.remote.webelement import WebElement

try:
    basestring  # attempt to evaluate basestring


    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)
    
class ElementFinder(object):

    def __init__(self):
        self._strategies = {
            'xpath': self._find_by_xpath,
            'id': self._find_by_id,
            'image' : self._find_by_image,
            'default': self._find_by_default
        }

    def find(self, application, locator, tag=None):
        assert application is not None
        assert locator is not None and len(locator) > 0
        (prefix, criteria) = self._parse_locator(locator)
        if prefix is None: 
            prefix = 'image' if (self._is_image_locator(locator)) else 'default'
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Element locator with prefix '" + prefix + "' is not supported")
        (tag, constraints) = self._get_tag_and_constraints(tag)
        return strategy(application, criteria, tag, constraints)

    def _is_image_locator(self, locator):
        return isinstance(locator, str) and (locator.endswith(('.png', '.jpg', '.jpeg')))

    def _find_by_xpath(self, application, criteria, tag, constraints):
        print(f"xpath criteria: {criteria}")
        return self._filter_elements(
            application.find_elements(by=AppiumBy.XPATH, value=criteria),
            tag, constraints)

    def _find_by_id(self, application, criteria, tag, constraints):
        print(f"id criteria: {criteria}")
        return self._filter_elements(
            application.find_elements(by=AppiumBy.ID, value=criteria),
            tag, constraints)

    def _find_by_image(self, application, criteria, tag, constraints):
        return self._filter_elements(
            application.find_elements(by=AppiumBy.IMAGE, value=self._image_to_base64(criteria)),
            tag, constraints)

    def _find_by_default(self, application, criteria, tag, constraints):
        if criteria.startswith('//'):
            return self._find_by_xpath(application, criteria, tag, constraints)
        return self._find_by_id(application, criteria, tag, constraints)

    # Private

    def _get_tag_and_constraints(self, tag):
        if tag is None:
            return None, {}

        tag = tag.lower()
        constraints = {}
        if tag == 'link':
            tag = 'a'
        elif tag == 'image':
            tag = 'img'
        elif tag == 'list':
            tag = 'select'
        elif tag == 'radio button':
            tag = 'input'
            constraints['type'] = 'radio'
        elif tag == 'checkbox':
            tag = 'input'
            constraints['type'] = 'checkbox'
        elif tag == 'text field':
            tag = 'input'
            constraints['type'] = 'text'
        elif tag == 'file upload':
            tag = 'input'
            constraints['type'] = 'file'
        return tag, constraints

    def _element_matches(self, element, tag, constraints):
        if not element.tag_name.lower() == tag:
            return False
        for name in constraints:
            if not element.get_attribute(name) == constraints[name]:
                return False
        return True

    def _filter_elements(self, elements, tag, constraints):
        elements = self._normalize_result(elements)
        if tag is None:
            return elements
        return filter(
            lambda element: self._element_matches(element, tag, constraints),
            elements)

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        return (prefix, criteria)

    def _normalize_result(self, elements):
        if not isinstance(elements, list):
            logger.debug("WebDriver find returned %s" % elements)
            return []
        return elements

    def _element_find(self, locator, first_only, required, tag=None):
        application = self._current_application()
        elements = None
        if isstr(locator):
            _locator = locator
            elements = self.find(application, _locator, tag)
            if required and len(elements) == 0:
                if self._is_image_locator(locator) : 
                    raise ValueError("Image at '" + locator + "' did not match any elements.")
                else:
                    raise ValueError("Element locator '" + locator + "' did not match any elements.")
            if first_only:
                if len(elements) == 0: return None
                return elements[0]
        elif isinstance(locator, WebElement):
            if first_only:
                return locator
            else:
                elements = [locator]
            return elements