#!/usr/bin/python3
# -*- encoding=utf8 -*-

from base.base_page import BasePage
from base.elements import Element


class FirstPage(BasePage):

    warning_confirm_button = Element('id', 'android:id/button1')
    slow_motion_checkbox = Element('id', 'slow_motion')
    button1 = Element('id', 'btn_1')
