#!/usr/bin/python3
# -*- encoding=utf8 -*-

from base.myapp import MyApp


def test_check_btn1(android):
    app = MyApp(android)

    app.login = 'myuser'

    app.slow_motion_checkbox.click()
    app.button1.click()

    assert False
