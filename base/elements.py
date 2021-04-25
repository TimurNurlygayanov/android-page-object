#!/usr/bin/python3
# -*- encoding=utf8 -*-


class Element():
    _locator = ('', '')
    _driver = None
    _wait_after_click = False

    def __init__(self, locator_type, locator_str):
        self._locator = (locator_type, locator_str)

    def find(self, timeout=10):
        element = None

        try:
            if self._locator[0] == 'id':
                # To make elements locators smaller:
                locator = self._locator[1]
                if ':' not in self._locator[1]:
                    app_name = self._driver.desired_capabilities['appPackage']
                    locator = '{0}:id/' + self._locator[1]
                    locator = locator.format(app_name)

                element = self._driver.find_element_by_id(locator)

            else:
                element = self._driver.find_element_by_xpath(self._locator[1])
        except Exception as e:
            print('Can not find element', self._locator)
            print(e)

    def clear(self):
        pass

    def click(self):
        element = self.find()

        if element:
            element.click()

    def send_keys(self, value):
        element = self.find()

        if element:
            element.send_keys(value)

    def _set_value(self, driver, value, clear=True):
        """ Set value to the input element. """

        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value)
