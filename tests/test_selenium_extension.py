# -*- coding: utf-8 -*-

import os

import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from mock import Mock, MagicMock
from mock import patch

from seismograph.ext.selenium.extension import Selenium
from .lib.factories import selenium_config_factory
from seismograph.ext.selenium import drivers
import seismograph.ext.selenium.browser as browser

from seismograph.ext.selenium.drivers import FirefoxWebDriver

from seismograph.ext.selenium.exceptions import SeleniumExError


class SeleniumTestCase(unittest.TestCase):
    """Tests for `Selenium` class.

    """

    def setUp(self):
        pass
        # self.selenium = Selenium()

    def tearDown(self):
        pass

    def test_firefox_with_empty_firefox_config(self):
        """Test `firefox` method.

        Note:
            Test to throw exception when firefox config in general selenium config exists but is empty.

        """
        selenium_config = {'FIREFOX': {}}
        mock = MagicMock()
        mock.get.side_effect = selenium_config.get

        s = Selenium(mock)
        with self.assertRaises(SeleniumExError) as context:
            s.firefox()
        self.assertTrue(
            'settings for firefox browser is not found in config' in context.exception
        )

    def test_firefox_with_lack_firefox_config(self):
        """Test `firefox` method.

        Note:
            Test to throw exception when firefox config in general selenium config doesn't exist.

        """
        selenium_config = {}
        mock = MagicMock()
        mock.get.side_effect = selenium_config.get

        s = Selenium(mock)
        with self.assertRaises(SeleniumExError) as context:
            s.firefox()
        self.assertTrue(
            'settings for firefox browser is not found in config' in context.exception
        )

    def test_firefox_webdriver_init(self):
        """Test `firefox` method.

        Note:
            Test to create web driver by given firefox config.

        """
        selenium_config = MagicMock()
        with patch('seismograph.ext.selenium.browser.create') as browser_create_mock:
            browser_create_mock.return_value(None)
            s = Selenium(selenium_config)
            try:
                s.firefox()
            except WebDriverException:
                self.fail('firefox driver fails to create')

    @patch('seismograph.ext.selenium.browser.create')
    @patch('seismograph.ext.selenium.drivers.FirefoxWebDriver')
    def test_firefox_browser_creating(self, webdriver_create_mock, browser_create_mock):
        """Test `firefox` method.

        Note:
            Test passing args to create browser.

        """
        selenium_config = MagicMock()
        s = Selenium(selenium_config)
        webdriver = webdriver_create_mock.return_value
        browser_create_mock.return_value(None)
        s.firefox()
        browser_create_mock.assert_called_once_with(s, webdriver)

    @patch('seismograph.ext.selenium.browser.create')
    @patch('seismograph.ext.selenium.drivers.FirefoxWebDriver')
    def test_firefox_return_browser(self, webdriver_create_mock, browser_create_mock):
        """Test `firefox` method.

        Note:
            Test returning browser by `firefox` method.

        """
        selenium_config = MagicMock()
        s = Selenium(selenium_config)
        browser = browser_create_mock.return_value
        self.assertEqual(browser, s.firefox())


def main():
    unittest.main()


if __name__ == '__main__':
    main()
