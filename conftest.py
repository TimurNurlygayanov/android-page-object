#!/usr/bin/python3
# -*- encoding=utf8 -*-

import os
import pytest

from appium import webdriver
from uuid import uuid4


def get(env_variable, default_value):
    value = None
    try:
        value = str(os.environ[env_variable])
    except:
        pass

    return value or default_value


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def android(request):
    platform_name = get('PLATFORM_NAME', 'Android')
    platform_version = get('PLATFORM_VERSION', '10.0')
    app_link = get('APP_LINK', '')
    app_pkg = get('APP_PKG', 'at.markushi.reveal')
    app_activity = get('APP_ACTIVITY', '.MyActivity')
    appium_host = get('APPIUM_HOST', 'http://localhost:4723/wd/hub')

    capabilities = {
        'platformName': platform_name,
        'platformVersion': platform_version,
        'appPackage': app_pkg,
        'appActivity': app_activity
    }

    if app_link:
        capabilities['app'] = app_link

    driver = webdriver.Remote(appium_host, capabilities)

    yield driver

    if request.node.rep_call.failed:
        # Make the screenshot if test failed:
        try:
            driver.save_screenshot('screenshots/failed_' + str(uuid4()) + '.png')
        except Exception as e:
            print(e)   # print exception, but do not raise it


def get_test_case_docstring(item):
    """ This function gets doc string from test case and format it
        to show this docstring instead of the test case name in reports.
    """

    full_name = ''

    if item._obj.__doc__:
        # Remove extra whitespaces from the doc string:
        name = str(item._obj.__doc__.split('.')[0]).strip()
        full_name = ' '.join(name.split())

        # Generate the list of parameters for parametrized test cases:
        if hasattr(item, 'callspec'):
            params = item.callspec.params

            res_keys = sorted([k for k in params])
            # Create List based on Dict:
            res = ['{0}_"{1}"'.format(k, params[k]) for k in res_keys]
            # Add dict with all parameters to the name of test case:
            full_name += ' Parameters ' + str(', '.join(res))
            full_name = full_name.replace(':', '')

    return full_name


def pytest_itemcollected(item):
    """ This function modifies names of test cases "on the fly"
        during the execution of test cases.
    """

    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)


def pytest_collection_finish(session):
    """ This function modified names of test cases "on the fly"
        when we are using --collect-only parameter for pytest
        (to get the full list of all existing test cases).
    """

    if session.config.option.collectonly is True:
        for item in session.items:
            # If test case has a doc string we need to modify it's name to
            # it's doc string to show human-readable reports and to
            # automatically import test cases to test management system.
            if item._obj.__doc__:
                full_name = get_test_case_docstring(item)
                print(full_name)

        pytest.exit('Done!')
