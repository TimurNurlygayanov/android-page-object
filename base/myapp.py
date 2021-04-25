#!/usr/bin/python3
# -*- encoding=utf8 -*-

from base.app import App
from base.elements import Element
from base.elements import ManyElement


class MyApp(App):

    warning_confirm_button = Element('id', 'android:id/button1')
    slow_motion_checkbox = Element('id', 'slow_motion')
    button1 = Element('id', 'btn_1')

    my_elements = ManyElement('id', 'new_id')
