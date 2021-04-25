#!/usr/bin/python3
# -*- encoding=utf8 -*-


class App():
    _driver = None

    def __init__(self, driver):
        self._driver = driver

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self.__getattribute__(name)._set_value(self._driver, value)
        else:
            super(App, self).__setattr__(name, value)

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if not item.startswith('_') and not callable(attr):
            attr._driver = self._driver
            attr._app = self

        return attr
