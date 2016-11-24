# -*- coding: utf-8 -*-

import logging

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from . import drivers
from . import browser
from .polling import POLLING_EXCEPTIONS
from ...utils.common import waiting_for
from .exceptions import SeleniumExError


logger = logging.getLogger(__name__)


EX_NAME = 'selenium'
DEFAULT_GET_BROWSER_DELAY = 0.5
DEFAULT_GET_BROWSER_TIMEOUT = 10
DEFAULT_BROWSER = drivers.FIREFOX

# DesiredCapabilities - задает параметры браузера
# {'platform': 'ANY', 'browserName': 'firefox', 'version': '', 'marionette': True, 'javascriptEnabled': True} 
DRIVER_TO_CAPABILITIES = {
    drivers.OPERA: DesiredCapabilities.OPERA,
    drivers.CHROME: DesiredCapabilities.CHROME,
    drivers.FIREFOX: DesiredCapabilities.FIREFOX,
    drivers.PHANTOMJS: DesiredCapabilities.PHANTOMJS,
    drivers.IE: DesiredCapabilities.INTERNETEXPLORER,
}


def get_capabilities(driver_name):
    """
    Get capabilities of driver

    :param driver_name: driver name
    :type driver_name: str
    """
    try:
        return DRIVER_TO_CAPABILITIES[driver_name]
    except KeyError:
        # ASK: зачем он ищет вхождение подстроку driver_name в другой строке
        raise SeleniumExError(
            'Capabilities for driver "{}" is not found'.find(driver_name),
        )


class Selenium(object):

    # !передаем только config
    # (browser_name, browser, is_running нет - их указываем в start или берем из config)
    def __init__(self, config):
        self.__config = config

        # ASK: где он инициализируется
        self.__browser = None
        self.__is_running = False
        self.__browser_name = None

    # эти 2 метода для возможности использования внутри
    # конструкции with (enter при инициализации через as, exit при выходе)
    def __enter__(self):
        self.start()
        return self.__browser

    def __exit__(self, *args, **kwargs):
        self.stop()

    # getter self.config => self.__config
    @property
    def config(self):
        return self.__config

    # getter
    @property
    def browser(self):
        return self.__browser

    # getter
    @property
    def browser_name(self):
        return self.__browser_name

    # getter
    @property
    def is_running(self):
        return self.__is_running

    def start(self, browser_name=None, timeout=None, delay=None):
        if not self.__is_running:
            self.__browser_name = (
                browser_name or self.__config.get('DEFAULT_BROWSER', DEFAULT_BROWSER)
            ).lower()

            def get_browser(func, *args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except POLLING_EXCEPTIONS:
                    return None

            def get_local_browser(browser_name):
                method = getattr(self, browser_name, None)

                if method:
                    return method()

                raise SeleniumExError(
                    'Incorrect browser name "{}"'.format(browser_name),
                )

            delay = delay or self.__config.get(
                'POLLING_DELAY', DEFAULT_GET_BROWSER_DELAY,
            )
            timeout = timeout or self.__config.get(
                'POLLING_TIMEOUT', DEFAULT_GET_BROWSER_TIMEOUT,
            )

            # вызов функции get_local_browser или self.remote с aргументом browser_name
            # get_local_browser возвращает просто название браузера
            args = {
                True: (self.remote, self.__browser_name),
                False: (get_local_browser, self.__browser_name),
            }

            # функция get_browser вызывается c args и kwargs до тех пор, пока не вызывается 
            # повторы вызова c шагом delay
            # и общем временем попыток вызова timeout
            # иначе выкинет иссключение exc_cls=SeleniumExError с message
            self.__browser = waiting_for(
                get_browser,
                delay=delay,
                timeout=timeout,
                exc_cls=SeleniumExError,
                args=args[bool(self.__config.get('USE_REMOTE', False))],
                message='Browser "{}" has not been started for "{}" sec.'.format(
                    self.__browser_name, timeout,
                ),
            )

            self.__is_running = True

    def stop(self):
        if self.__is_running:
            with self.__browser.disable_polling():
                self.__browser.close()
                self.__browser.quit()
            self.__is_running = False

    def remote(self, driver_name):
        driver_name = driver_name.lower()
        # FIX: .get('REMOTE', default_value_needed)
        remote_config = self.__config.get('REMOTE')

        if not remote_config:
            raise SeleniumExError(
                'settings for remote is not found in config',
            )

        logger.debug(
            'Remote config: {}'.format(str(remote_config)),
        )

        # FIX: .get('desired_capabilities', default_value_needed)
        if not remote_config.get('desired_capabilities'):
            capabilities = get_capabilities(driver_name)
            # FIX: remote_config.pop('capabilities', {}) - удаляет пару key-value
            # и возвращает value (видимо, должен быть словарем), а если не словарь 
            # (к примеру list, тогда .get(driver_name, {}) сломается
            # get(driver_name, {}) может быть не словарем, тогда capabilities.update(
            # сломется

            capabilities.update(
                remote_config.pop('capabilities', {}).get(driver_name, {}),
            )
            remote_config['desired_capabilities'] = capabilities

        # ASK: что делает drivers.RemoteWebDriver
        driver = drivers.RemoteWebDriver(**remote_config)
        # ASK: откуда взялся browser
        return browser.create(self, driver)

    def ie(self):
        ie_config = self.__config.get('IE')

        if not ie_config:
            raise SeleniumExError(
                'settings for ie browser is not found in config',
            )

        logger.debug(
            'Ie config: {}'.format(str(ie_config)),
        )

        driver = drivers.IeWebDriver(**ie_config)
        return browser.create(self, driver)

    def chrome(self):
        """
        :rtype: selenium.webdriver.chrome.webdriver.WebDriver
        """
        chrome_config = self.__config.get('CHROME')

        if not chrome_config:
            raise SeleniumExError(
                'settings for chrome browser is not found in config',
            )

        logger.debug(
            'Chrome config: {}'.format(str(chrome_config)),
        )

        driver = drivers.ChromeWebDriver(**chrome_config)
        return browser.create(self, driver)

    def firefox(self):
        firefox_config = self.__config.get('FIREFOX', {})

        logger.debug(
            'Firefox config: {}'.format(str(firefox_config)),
        )

        driver = drivers.FirefoxWebDriver(**firefox_config)
        return browser.create(self, driver)

    def phantomjs(self):
        phantom_config = self.__config.get('PHANTOMJS')

        if not phantom_config:
            raise SeleniumExError(
                'settings for phantom js is not found in config',
            )

        logger.debug(
            'PhantomJS config: {}'.format(str(phantom_config)),
        )

        driver = drivers.PhantomJSWebDriver(**phantom_config)
        return browser.create(self, driver)

    def opera(self):
        opera_config = self.__config.get('OPERA')

        if not opera_config:
            raise SeleniumExError(
                'settings for opera browser is not found in config',
            )

        logger.debug(
            'Opera config: {}'.format(str(opera_config)),
        )

        driver = drivers.OperaWebDriver(**opera_config)
        return browser.create(self, driver)
