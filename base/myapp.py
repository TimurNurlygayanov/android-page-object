#!/usr/bin/python3
# -*- encoding=utf8 -*-

from base.app import App
from base.elements import Element


class MyApp(App):

    warning_confirm_button = Element('id', 'android:id/button1')
    slow_motion_checkbox = Element('id', 'slow_motion')
    button1 = Element('id', 'btn_1')

    my_elements = Element('id', 'new_id', many_elements=True)
