#!/usr/bin/python3
# -*- encoding=utf8 -*-


class Element():
    _locator = ('', '')
    _driver = None
    _wait_after_click = False

    def __init__(self, locator_type, locator_str):
        self._locator = (locator_type, locator_str)

    def find(self, many=False):
        result = None

        try:
            if self._locator[0] == 'id':
                locator = self._locator[1]

                # To make elements locators smaller:
                if ':' not in self._locator[1]:
                    app_name = self._driver.desired_capabilities['appPackage']
                    locator = '{0}:id/' + self._locator[1]
                    locator = locator.format(app_name)

                if many_elements:
                    result = self._driver.find_elements_by_id(locator)
                else:
                    result = self._driver.find_element_by_id(locator)

            else:
                result = self._driver.find_element_by_xpath(self._locator[1])
        except Exception as e:
            print('Can not find element', self._locator)
            print(e)

        return result

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
