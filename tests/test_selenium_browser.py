# -*- coding: utf-8 -*-

import unittest
from mock import MagicMock

from selenium.webdriver.remote.webdriver import WebDriver
from seismograph.ext.selenium.browser import BrowserConfig, create, change_config
from seismograph.ext.selenium.extension import Selenium, DEFAULT_BROWSER
from seismograph.ext.selenium.proxy import WebDriverProxy


class BrowserConfigTestCase(unittest.TestCase):
    """Tests for `BrowserConfig` class in `browser.py` module.

    """

    def setUp(self):
        selenium_config = {
            'PAGE_LOAD_TIMEOUT': None,
            'SCRIPT_TIMEOUT': None,
            'WAIT_TIMEOUT': None,
            'WINDOW_SIZE': None,
            'MAXIMIZE_WINDOW': None
        }
        mock_selenium_config = MagicMock()
        mock_selenium_config.get.side_effect = selenium_config.get
        self.selenium = Selenium(mock_selenium_config)
        self.driver = MagicMock()

    def tearDown(self):
        pass

    def test_set_page_load_timeout(self):
        """Test `PAGE_LOAD_TIMEOUT` class attribute setter.

        Note:
            Test calling appropriate driver method with right args.

        """
        set_page_load_timeout = 100500
        self.driver.set_page_load_timeout = MagicMock()

        b = BrowserConfig(self.selenium, self.driver)
        b.PAGE_LOAD_TIMEOUT = set_page_load_timeout

        self.driver.set_page_load_timeout.assert_called_once_with(set_page_load_timeout)

    def test_set_page_script_timeout(self):
        """Test `SCRIPT_TIMEOUT` class attribute setter.

        Note:
            Test calling appropriate driver method with right args.

        """
        set_script_timeout = 228
        self.driver.set_script_timeout = MagicMock()

        b = BrowserConfig(self.selenium, self.driver)
        b.SCRIPT_TIMEOUT = set_script_timeout

        self.driver.set_script_timeout.assert_called_once_with(set_script_timeout)

    def test_set_page_wait_timeout(self):
        """Test `WAIT_TIMEOUT` class attribute setter.

        Note:
            Test calling appropriate driver method with right args.

        """
        set_wait_timeout = 322
        self.driver.implicitly_wait = MagicMock()

        b = BrowserConfig(self.selenium, self.driver)
        b.WAIT_TIMEOUT = set_wait_timeout

        self.driver.implicitly_wait.assert_called_once_with(set_wait_timeout)

    def test_set_page_window_size(self):
        """Test `WINDOW_SIZE` class attribute setter.

        Note:
            Test calling appropriate driver method with right args.

        """
        set_width = 123
        set_height = 456
        self.driver.set_window_size = MagicMock()

        b = BrowserConfig(self.selenium, self.driver)
        b.WINDOW_SIZE = (set_width, set_height)

        self.driver.set_window_size.assert_called_once_with(set_width, set_height)

    def test_set_page_maximize_window(self):
        """Test `MAXIMIZE_WINDOW` class attribute setter.

        Note:
            Test calling appropriate driver method with right args.

        """
        self.driver.maximize_window = MagicMock()

        set_maximize_window_size = 31415926

        b = BrowserConfig(self.selenium, self.driver)
        b.MAXIMIZE_WINDOW = set_maximize_window_size

        self.driver.maximize_window.assert_called_once_with()


class ChangeConfigFunctionTestCase(unittest.TestCase):
    """Tests for `change_config` function in `browser.py` module.

    """
    def setUp(self):
        self.selenium_config = {
            'WAIT_TIMEOUT': 1488,
            'POLLING_DELAY': 42,
            'POLLING_TIMEOUT': 1407,
            'PAGE_LOAD_TIMEOUT': 11235813
        }
        mock_selenium_config = MagicMock()
        mock_selenium_config.get.side_effect = self.selenium_config.get
        selenium = Selenium(mock_selenium_config)

        driver = MagicMock(spec=WebDriver)
        browser_config = BrowserConfig(selenium, driver)

        self.browser = WebDriverProxy(driver, browser_config)

    def tearDown(self):
        pass

    def test_change_config_set_wait_timeout(self):
        """Test `change_config` function.

        Note:
            Test changing `WAIT_TIMEOUT` attribute of class `WebDriverProxy`
            by this function.

        """
        set_wait_timeout = 228
        with change_config(self.browser, wait_timeout=set_wait_timeout):
            self.assertEqual(self.browser.config.WAIT_TIMEOUT, set_wait_timeout)

    def test_change_config_set_polling_delay(self):
        """Test `change_config` function.

        Note:
            Test changing `POLLING_DELAY` attribute of class `WebDriverProxy`
            by this function.

        """
        set_polling_delay = 228
        with change_config(self.browser, polling_delay=set_polling_delay):
            self.assertEqual(self.browser.config.POLLING_DELAY, set_polling_delay)

    def test_change_config_set_polling_timeout(self):
        """Test `change_config` function.

        Note:
            Test changing `POLLING_TIMEOUT` attribute of class `WebDriverProxy`
            by this function.

        """
        set_polling_timeout = 228
        with change_config(self.browser, polling_timeout=set_polling_timeout):
            self.assertEqual(self.browser.config.POLLING_TIMEOUT, set_polling_timeout)

    def test_change_config_set_page_load_timeout(self):
        """Test `change_config` function.

        Note:
            Test changing `PAGE_LOAD_TIMEOUT` attribute of class `WebDriverProxy`
            by this function.

        """
        set_page_load_timeout = 228
        with change_config(self.browser, page_load_timeout=set_page_load_timeout):
            self.assertEqual(self.browser.config.PAGE_LOAD_TIMEOUT, set_page_load_timeout)

    def test_change_config_check_restore(self):
        """Test `change_config` function.

        Note:
            Test restoring initial `PAGE_LOAD_TIMEOUT`, `POLLING_TIMEOUT`,
            `POLLING_DELAY` and `WAIT_TIMEOUT` values out of `with`
            context manager.

        """
        set_value = 322
        with change_config(
                self.browser,
                page_load_timeout=set_value,
                wait_timeout=set_value,
                polling_delay=set_value,
                polling_timeout=set_value):
            pass

        restored_values = {
            'WAIT_TIMEOUT': self.browser.config.WAIT_TIMEOUT,
            'POLLING_DELAY': self.browser.config.POLLING_DELAY,
            'POLLING_TIMEOUT': self.browser.config.POLLING_TIMEOUT,
            'PAGE_LOAD_TIMEOUT': self.browser.config.PAGE_LOAD_TIMEOUT
        }
        self.assertItemsEqual(restored_values.items(), self.selenium_config.items())


class CreateFunctionTestCase(unittest.TestCase):
    """Tests for `create` function in `browser.py` module.

    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_check_set_reason_storage(self):
        """Test function `create`.

        Note:
            Test setting `browser_name` for `reason_storage`.

        """
        pass
        # TODO
        # selenium = MagicMock()
        # selenium.side_effect = Selenium
        # selenium = selenium.side_effect(MagicMock())
        # setattr(selenium, '_Selenium__browser_name', DEFAULT_BROWSER)

        # driver = MagicMock(spec=WebDriver)

        # browser = MagicMock()
        # browser.side_effect = WebDriverProxy
        # browser = browser.side_effect(
        #     driver, config=BrowserConfig(selenium, driver)
        # )
        # browser.reason_storage.__setitem__ = dict().__setitem__
        # browser.reason_storage.__getitem__ = dict().__getitem__

        # # with patch('seismograph.ext.selenium.proxy.WebDriverProxy') as mock_driver_proxy:
        # #     print(mock_driver_proxy, 'test')
        # #     mock_driver_proxy.return_value = browser
        # create(selenium, driver)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
