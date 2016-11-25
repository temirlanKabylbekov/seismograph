# -*- coding: utf-8 -*-

import os

import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from mock import Mock, MagicMock
from mock import patch

from seismograph.ext.selenium.extension import Selenium, DEFAULT_BROWSER, DRIVER_TO_CAPABILITIES
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

    # tests for `firefox` method
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

    # tests for `remote` method
    def test_remote_with_empty_remote_config(self):
        """Test `remote` method.

        Note:
            Test to throw exception when remote browser config in
            general selenium config exists but is empty.

        """
        selenium_config = {'REMOTE': {}}
        mock_config = MagicMock(name='selenium_config')
        mock_config.get.side_effect = selenium_config.get

        mock_driver = MagicMock(name='driver_name')

        s = Selenium(mock_config)
        with self.assertRaises(SeleniumExError) as context:
            s.remote(mock_driver)
        self.assertTrue(
            'settings for remote is not found in config' in context.exception
        )

    @patch('seismograph.ext.selenium.browser.create')
    @patch('seismograph.ext.selenium.drivers.RemoteWebDriver')
    def test_remote_set_desired_capabilities_config(
            self, webdriver_create_mock, browser_create_mock):
        """Test `remote` method.

        Note:
            Test setting `desired_capabilities` in remote browser config with
            this empty property.

        """
        selenium_config = {'REMOTE': {'desired_capabilities': {}}}
        mock_config = MagicMock(name='selenium_config')
        mock_config.get.side_effect = selenium_config.get

        s = Selenium(mock_config)
        s.remote(DEFAULT_BROWSER)
        self.assertEqual(
            mock_config.get('REMOTE').get('desired_capabilities'),
            DRIVER_TO_CAPABILITIES[DEFAULT_BROWSER]
        )

    @patch('seismograph.ext.selenium.browser.create')
    @patch('seismograph.ext.selenium.drivers.RemoteWebDriver')
    def test_remote_set_desired_capabilities_config(
            self, webdriver_create_mock, browser_create_mock):
        """Test `remote` method.

        Note:
            Test removing `capabilities` after setting `desired_capabilities` in 
            remote browser config with this empty property.

        """
        selenium_config = {
            'REMOTE': {
                'desired_capabilities': {},
                'capabilities': {
                    'driver_name': DEFAULT_BROWSER
                }
            }
        }
        mock_config = MagicMock(name='selenium_config')
        mock_config.get.side_effect = selenium_config.get
        mock_config.__contains__.side_effect = selenium_config.__contains__

        s = Selenium(mock_config)
        s.remote(DEFAULT_BROWSER)

        self.assertTrue(
            'capabilities' not in mock_config.get('REMOTE')
        )

    def test_remote_webdriver_init(self):
        """Test `remote` method.

        Note:
            Test to create web driver by given remote browser config.

        """
        selenium_config = {
            'REMOTE': {
                'desired_capabilities': DRIVER_TO_CAPABILITIES[DEFAULT_BROWSER],
            }
        }
        mock_config = MagicMock()
        mock_config.get.side_effect = selenium_config.get

        with patch('seismograph.ext.selenium.browser.create') as browser_create_mock:
            browser_create_mock.return_value(None)
            s = Selenium(mock_config)
            try:
                s.remote(DEFAULT_BROWSER)
            except WebDriverException:
                self.fail('remote driver fails to create')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
