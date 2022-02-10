#!/usr/bin/python3
# -*- encoding=utf8 -*-

from pages.first_page import FirstPage


def test_check_btn1(android):
    app = FirstPage(android)

    app.login = 'myuser'

    app.slow_motion_checkbox.click()
    app.button1.click()

    assert app.login.ex