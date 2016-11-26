# -*- coding: utf-8 -*-

import unittest
from mock import MagicMock, patch

from seismograph.ext.selenium.browser import (
    BrowserConfig
)
from seismograph.ext.selenium.extension import (
    Selenium, DEFAULT_BROWSER, DRIVER_TO_CAPABILITIES, get_capabilities
)


class BrowserConfigTestCase(unittest.TestCase):
    """Tests for `BrowserConfig` class.

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


class StandaloneFunctionsTestCase(unittest.TestCase):
    """Tests for standalone functions in `browser.py` module.

    """
    def test_create_check_set_reason_storage(self):
        """Test function `create`.

        Note:
            Test setting `browser_name` for `reason_storage`.

        """
        pass

    def test_change_config_set_wait_timeout(self):
        pass

    def test_change_config_set_polling_delay(self):
        pass

    def test_change_config_set_polling_timeout(self):
        pass

    def test_change_config_set_page_load_timeout(self):
        pass

    def test_change_config_check_keep_restoring(self):
        pass

    def test_change_config_check_restore(self):
        pass



def main():
    unittest.main()


if __name__ == '__main__':
    main()
