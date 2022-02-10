#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time
import logging
import pytest
import cv2

from pathlib import Path

from uuid import uuid4
from skimage.io import imread
from skimage.metrics import structural_similarity

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.pointer_input import PointerInput


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BasePage:
    driver = None

    def __init__(self, driver):
        self.driver = driver

    def __setattr__(self, name, value):
        if name != 'driver':
            self.__getattribute__(name)._set_value(self._driver, value)
        else:
            super(BasePage, self).__setattr__(name, value)

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if item != 'driver' and not callable(attr):
            attr.driver = self.driver
            attr.app = self

        return attr

    def click_by_coords(self, x_coord: int = 1, y_coord: int = 1):
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver,
                                            mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(x=x_coord, y=y_coord)
        actions.w3c_actions.pointer_action.click()
        actions.w3c_actions.key_action.pause(1)
        actions.w3c_actions.perform()

    def verify_by_screenshot(self, reference_name, expected_rate=0.96,
                             timeout=10.0):
        """ This function returns the number which helps to
            understand if two images are identical or not.
            For two identical images the score is 1.0
            For different images the score will be less than 1.0
        """

        platform_name = self.driver.desired_capabilities['platformName']
        platform_name = platform_name.lower()

        start_time = time.time()
        current_page = f'screenshots/{uuid4()}.png'
        diff_save = f'screenshots/diff_{uuid4()}.png'
        self.screenshot(current_page)

        screenshot = imread(current_page)
        height, width = screenshot.shape[:-1]

        ref_path = f'{platform_name}_{height}x{width}_'
        ref_image_name = f'{ref_path}{reference_name}.png'
        ref_image = self.get_reference_screenshot(ref_image_name)

        # If ref screenshot doesn't exist - create new one:
        if not ref_image:
            self.save_reference_screenshot(ref_image_name)
            pytest.skip(f'Created new ref screenshot {ref_image_name}')
        else:
            score = 0.0
            while score < expected_rate and timeout > 0:
                self.screenshot(current_page)
                img1 = imread(current_page)
                img2 = imread(ref_image)

                score, diff = structural_similarity(
                    img1, img2, full=True, multichannel=True
                )

                if score < expected_rate:
                    diff = (diff * 255).astype('uint8')
                    cv2.imwrite(diff_save, diff)

                    # Wait when page will be ready
                    time.sleep(0.2)
                    timeout -= time.time() - start_time

                logger.debug(f'Image compare score: {score}')
                logger.debug(f'Ref image {ref_image}')
                logger.debug(f'Current page image {current_page}')

            msg = 'Screenshot of the page does not match the reference'
            assert round(score, 3) >= expected_rate, msg

    def get_reference_screenshot(self, ref_image):
        """ Get reference screenshot. """

        # Check if references directory exists and create it if it doesn't exist:
        Path('references').mkdir(parents=True, exist_ok=True)

        return f'references/{ref_image}'

    def save_reference_screenshot(self, ref_image):
        """ Make a reference screenshot. """

        ref_image = f'references/{ref_image}'

        time.sleep(5)  # make sure page will be ready
        self.screenshot(ref_image)
