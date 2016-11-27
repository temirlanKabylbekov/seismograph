# -*- coding: utf-8 -*-

import unittest
from mock import MagicMock, patch
from selenium.common.exceptions import WebDriverException

from seismograph.ext.selenium.extension import Selenium, DEFAULT_BROWSER, \
    DRIVER_TO_CAPABILITIES, get_capabilities
from seismograph.ext.selenium.exceptions import SeleniumExError


class SeleniumStartMethodTestCase(unittest.TestCase):
    """Tests for `Selenium` class `start` method.

    """
    def setUp(self):
        selenium_config = MagicMock()
        self.selenium = Selenium(selenium_config)

    def tearDown(self):
        pass

    # TO CODE REVIEWER: мок waiting_for работает только для абсолютного
    # импорта waiting_for в модуле extension.py,
    # в случае текущего импорта - относительного, мок не работает!
    # в чем причина и как быть в случае относительного импорта?
    @patch('seismograph.utils.common.waiting_for')
    def test_start_check_setting_browser_name(self, mock_waiting_for):
        """Test for `start` method.

        Note:
            Test to set `browser_name` via passing arg in this method.

        """
        mock_waiting_for.return_value = None
        browser_name = 'chrome'
        self.selenium.start(browser_name=browser_name)
        self.assertEqual(self.selenium._Selenium__browser_name, browser_name)

    @patch('seismograph.utils.common.waiting_for')
    def test_start_check_setting_delay(self, mock_waiting_for):
        """Test for `start` method.

        Note:
            Test to set `delay` and pass like arg to `waiting_for` function.

        """
        mock_waiting_for.return_value = None
        browser_delay = 7
        self.selenium.start(delay=browser_delay)
        args, kwargs = mock_waiting_for.call_args
        self.assertEqual(kwargs['delay'], browser_delay)

    @patch('seismograph.utils.common.waiting_for')
    def test_start_check_setting_timeout(self, mock_waiting_for):
        """Test for `start` method.

        Note:
            Test to set `timeout` and pass like arg to `waiting_for` function.

        """
        mock_waiting_for.return_value = None
        browser_timeout = 88
        self.selenium.start(timeout=browser_timeout)
        args, kwargs = mock_waiting_for.call_args
        self.assertEqual(kwargs['timeout'], browser_timeout)

    # TO CODE REVIEWER: есть ли возможность замокать вложенную функцию, объявленной 
    # внутри другой функции. stackoverflow говорит, что нет, но мне 
    # что-то подсказывает, что можно
    def test_start_check_get_local_browser_with_invalid_browser_name(self):
        """Test `start` method.

        Note:
            Test nested function `get_local_browser` by passing invalid
            browser name.

        """
        pass

    def test_start_check_get_local_browser_with_valid_browser_name(self):
        """Test `start` method.

        Note:
            Test nested function `get_local_browser` by passing valid
            browser name.

        """
        pass

    @patch('seismograph.utils.common.waiting_for')
    def test_start_check_is_running_equals_true(self, mock_waiting_for):
        """Test `start` method.

        Note:
            Test that `is_running` class attribute equals `True` after
            executing `start` method.

        """
        mock_waiting_for.return_value = None
        self.selenium.start()
        self.assertTrue(self.selenium.is_running)


class SeleniumStartMethodCallBrowserTestCase(unittest.TestCase):
    """Tests for `Selenium` class `start` method calling browser.

    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('seismograph.utils.common.waiting_for', return_value=None)
    def test_start_check_calling_remote_browser(self, mock_waiting_for):
        """"Test `start` method.

        Note:
            Test calling remote browser when passing
            `USE_REMOTE` true flag in selenium config file.

        """
        selenium_config = {'USE_REMOTE': True}
        mock = MagicMock()
        mock.get.side_effect = selenium_config.get

        s = Selenium(mock)
        s.start()
        args, kwargs = mock_waiting_for.call_args
        self.assertEqual(kwargs['args'][0].__name__, 'remote')

    @patch('seismograph.utils.common.waiting_for', return_value=None)
    def test_start_check_calling_local_browser(self, mock_waiting_for):
        """"Test `start` method.

        Note:
            Test calling local browser when passing
            `USE_REMOTE` false flag in selenium config file.

        """
        selenium_config = {'USE_REMOTE': False}
        mock = MagicMock()
        mock.get.side_effect = selenium_config.get

        s = Selenium(mock)
        s.start()
        args, kwargs = mock_waiting_for.call_args
        self.assertEqual(kwargs['args'][0].__name__, 'get_local_browser')


class SeleniumTestCase(unittest.TestCase):
    """Tests for `Selenium` class.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test `stop` method
    def test_stop_check_close_and_quit_executed(self):
        """Test `stop` method.

        Note:
            Test that `close` and `quit` methods were executed.

        """
        selenium_config = MagicMock()
        selenium = Selenium(selenium_config)
        setattr(selenium, '_Selenium__is_running', True)

        browser = MagicMock()
        browser.close = MagicMock()
        browser.quit = MagicMock()
        setattr(selenium, '_Selenium__browser', browser)

        selenium.stop()

        self.assertTrue(browser.close.called and browser.quit.called)

    def test_stop_check_is_running_equals_false(self):
        """Test `stop` method.

        Note:
            Test that `is_running` attribute after stop equals `False`.

        """
        mock_selenium_config = MagicMock()
        s = Selenium(mock_selenium_config)
        setattr(s, '_Selenium__is_running', True)
        setattr(s, '_Selenium__browser', MagicMock())
        s.stop()
        self.assertEqual(s.is_running, False)

    # TO CODE REVIEWER: поскольку, для других локальных браузеров тесты
    # будут одинаковыми, то не стали писать для них тесты. Ограничились
    # одним браузером firefox

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

    @unittest.skip('don\'t physically open local browser(debug purpose)')
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
    def test_remote_remove_capabilities_config_after_setting_desired(
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

    @unittest.skip('don\'t physically connect to remote browser (debug purpose)')
    def test_remote_webdriver_init(self):
        """Test `remote` method.

        Note:
            Test to create web driver by given remote browser config.

        """
        selenium_config = {
            'REMOTE': {
                'desired_capabilities': DRIVER_TO_CAPABILITIES[DEFAULT_BROWSER]
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


class StandaloneFunctionsTestCase(unittest.TestCase):
    """Tests for standalone functions in `extension.py` module.

    """
    def test_get_capabilities_pass_valid_driver(self):
        self.assertEqual(
            get_capabilities(DEFAULT_BROWSER),
            DRIVER_TO_CAPABILITIES[DEFAULT_BROWSER]
        )

    def test_get_capabilities_pass_invalid_driver(self):
        fake_driver_name = 'FAKE_DRIVER'
        with self.assertRaises(SeleniumExError) as context:
            get_capabilities(fake_driver_name)
        self.assertTrue(
            'Capabilities for driver "{}" is not found'.format(fake_driver_name)
            in context.exception
        )


def main():
    unittest.main()


if __name__ == '__main__':
    main()
