#!/usr/bin/python3
# -*- encoding=utf8 -*-

import os
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Element:
    locator = None
    driver = None
    wait_after_click = False

    def __init__(self, locator_type, locator_str):
        self.locator = {locator_type: locator_str}

    def find(self, timeout: float = 15.0, required=True):
        """ Find element. """

        element = None

        locator_type, locator_str = self._parse_locator()

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator_str))
            )
        except:
            msg = f'Element {locator_type} {locator_str} not found'
            logger.debug(msg)

        if required and not element:
            raise Exception('Element not found', self.locator)

        return element

    def click(self):
        element = self.find()

        if element:
            element.click()

    def send_keys(self, value):
        element = self.find()

        if element:
            element.send_keys(value)

    def is_present(self, timeout=10.0):
        """ Check is element exits. """

        element = self.find(timeout=timeout, required=False)
        return bool(element)

    def _parse_locator(self):
        """ Modify locator based on the platform and attributes. """

        platform_name = self.driver.desired_capabilities['platformName']
        platform_name = platform_name.lower()

        locator_type, locator_str = '', ''

        if platform_name == 'android':
            if 'id' in self.locator:
                locator_type = 'id'
                locator_str = self.locator['id']
                if ':' not in locator_str:
                    app_name = os.environ['APP_PACKAGE']
                    locator_str = f'{app_name}:id/{locator_str}'

            elif 'text' in self.locator:
                locator_type = 'xpath'
                locator_text = self.locator['text']
                locator_str = f'//*[@text="{locator_text}"]'

            elif 'contains_text' in self.locator:
                locator_type = 'xpath'
                xpath = '//*[contains(@text, "{0}")]'
                locator_str = xpath.format(self.locator['contains_text'])

            elif 'xpath' in self.locator:
                locator_type = 'xpath'
                locator_str = self.locator['xpath']

            elif 'accessibility id' in self.locator:
                locator_type = 'accessibility id'
                locator_str = self.locator['accessibility id']

            elif 'content_desc' in self.locator:
                locator_type = 'xpath'
                xpath = '//*[@content-desc="{0}"]'
                locator_str = xpath.format(self.locator['content_desc'])

        elif platform_name == 'ios':
            if 'label' in self.locator:
                locator_type = 'xpath'
                locator_str = self.locator['label']
                locator_str = f'//*[@label="{locator_str}"]'

        return locator_type, locator_str
