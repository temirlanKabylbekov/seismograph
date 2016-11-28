# -*- coding: utf-8 -*-

import unittest
from mock import MagicMock, patch, PropertyMock

from seismograph.ext.selenium.pageobject import ProxyObject, PageCache, \
    PageMeta, PageElement, _Base, Page, PageItem
from seismograph.ext.selenium.query import QueryObject, QueryResult


# nothing important to test
class ProxyObjectTestCase(unittest.TestCase):
    """Tests for `ProxyObject` class in `pageobject.py` module.

    """
    def setUp(self):
        pass

    def tearDown(self):
        pass


class PageCacheTestCase(unittest.TestCase):
    """Tests for `PageCache` class in `pageobject.py` module.

    """

    def setUp(self):
        self.stub_dict = {'key': 'value'}
        self.page_cache = PageCache(self.stub_dict)

    def tearDown(self):
        pass

    def test_restore(self):
        """Test `restore` method.

        Note:
            Test restoring initial value out of context manager.

        """
        with self.page_cache.restore():
            pass
        self.assertEqual(self.stub_dict, self.page_cache)

    def test_clear_when_entity_is_eternal(self):
        """Test `clear` method.

        Note:
            Test not to clear when entity is eternal.

        """
        setattr(self.page_cache, 'is_eternal', True)
        self.page_cache.clear()
        self.assertEqual(self.stub_dict, self.page_cache)

    def test_clear_when_entity_isnot_eternal(self):
        """Test `clear` method.

        Note:
            Test to clear when entity is not eternal.

        """
        setattr(self.page_cache, 'is_eternal', False)
        self.page_cache.clear()
        self.assertEqual({}, self.page_cache)


class PageElementTestCase(unittest.TestCase):
    """Tests for `PageElement` class in `pageobject.py` module.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test __init__ method
    def test_init_pass_not_args(self):
        """Test `__init__` method.

        Note:
            Test when passing neither one args.

        """
        with self.assertRaises(AssertionError) as context:
            page_element = PageElement()
        self.assertTrue(
            'Element can not be created without arguments' in context.exception
        )

    def test_init_pass_class_instance_of_type(self):
        """Test `__init__` method.

        Note:
            Test when passing class as arg which is instance of `type` class or
            `types.ClassType` for python 2.

        """
        instance_of_type_class = dict

        page_element = PageElement(instance_of_type_class)
        self.assertEqual(
            getattr(page_element, '_PageElement__class'), instance_of_type_class
        )

    @patch('seismograph.ext.selenium.pageobject.query_set')
    def test_init_pass_page_element_instance(self, mock_query_set):
        """Test `__init__` method.

        Note:
            Test when passing `PageElement` instance as arg.

        """
        stub_iter_object = range(3)
        mock_query_set.return_value = stub_iter_object

        arg_page_element = MagicMock(spec=PageElement)
        page_element = PageElement(arg_page_element)

        self.assertEqual(
            getattr(page_element, '_PageElement__query_set'),
            stub_iter_object
        )

    def test_init_pass_query_object_instance(self):
        """Test `__init__` method.

        Note:
            Test when passing `QueryObject` instance as arg.

        """
        query_object = MagicMock(spec=QueryObject)
        setattr(query_object, 'tag', 'tag')

        page_element = PageElement(query_object)
        self.assertEqual(
            getattr(page_element, '_PageElement__query_set')[0].tag,
            query_object.tag
        )

    def test_init_pass_invalid_arg(self):
        """Test `__init__` method.

        Note:
            Test when passing  invalid instance as arg.
            Invalid arg doesn't belong to `PageElement`, `QueryObject`
            and class instance of `type` class.

        """
        invalid_arg = dict()

        with self.assertRaises(ValueError) as context:
            page_element = PageElement(invalid_arg)
        self.assertTrue(
            'Incorrect page object argument {}'.format(invalid_arg) in
            context.exception
        )

    def test_init_pass_list_class_not_pass_is_class(self):
        """Test `__init__` method.

        Note:
            Test when passing  through `options` arg 'list_class' but
            not passing 'is_class' values.

        """
        arg = dict
        options = {
            'list_class': MagicMock()
        }

        with self.assertRaises(ValueError) as context:
            page_element = PageElement(arg, **options)
        self.assertTrue(
            '"list_class" can not be using without "is_list"' in
            context.exception
        )

    def test_init_pass_call_and_list_class(self):
        """Test `__init__` method.

        Note:
            Test when passing  through `options` arg 'call' and 'list_class'
            values.

        """
        arg = dict
        options = {
            'call': 'call_value',
            'list_class': list,
            'is_list': True
        }

        page_element = PageElement(arg, **options)

        changed_list_class = getattr(page_element, '_PageElement__list_class')

        self.assertEqual(changed_list_class.__name__, 'list')
        self.assertEqual(changed_list_class.__bases__, (list,))
        self.assertEqual(changed_list_class.__call__, 'call_value')

    def test_init_pass_call_and_we_class_not_pass_is_list(self):
        """Test `__init__` method.

        Note:
            Test when passing  through `options` arg 'call', 'we_class' and
            not passing `is_list` values.

        """
        arg = dict
        options = {
            'call': 'call_value',
            'we_class': list
        }

        page_element = PageElement(arg, **options)

        changed_we_class = getattr(page_element, '_PageElement__we_class')

        self.assertEqual(changed_we_class.__name__, 'list')
        self.assertEqual(changed_we_class.__bases__, (list,))
        self.assertEqual(changed_we_class.__call__, 'call_value')

    def test_init_pass_call_and_is_list_not_pass_we_class_and_list_class(self):
        """Test `__init__` method.

        Note:
            Test when passing  through `options` arg 'call', 'is_list' and
            not passing `we_class` and `list_class` values.

        """
        arg = dict
        options = {
            'call': 'call_value',
            'is_list': True
        }

        page_element = PageElement(arg, **options)

        changed_list_class = getattr(page_element, '_PageElement__list_class')

        self.assertEqual(changed_list_class.__name__, 'CallableObject')
        self.assertEqual(changed_list_class.__bases__, (ProxyObject,))
        self.assertEqual(changed_list_class.__call__, 'call_value')

    def test_init_pass_call_not_pass_we_class_and_list_class_and_is_list(self):
        """Test `__init__` method.

        Note:
            Test when passing  through `options` arg 'call', 'is_list' and
            not passing `we_class` and `list_class` values.

        """
        arg = dict
        options = {
            'call': 'call_value',
        }

        page_element = PageElement(arg, **options)

        changed_we_class = getattr(page_element, '_PageElement__we_class')

        self.assertEqual(changed_we_class.__name__, 'CallableObject')
        self.assertEqual(changed_we_class.__bases__, (ProxyObject,))
        self.assertEqual(changed_we_class.__call__, 'call_value')

    # test __key__
    def test_key(self):
        pass

    # test __query_set__
    def test_query_set(self):
        # TODO
        pass

    # test __get__
    def test_get(self):
        # TODO
        pass

    def test_make_object_get_from_cache(self):
        """Test `__make_object__` method.

        Note:
            Test to get result from page cache

        """
        with patch(
                'seismograph.ext.selenium.pageobject.Page.cache',
                new_callable=PropertyMock) as mock_page_cache:
            page = Page()

            page_element = PageElement(dict)
            mock_page_cache.return_value = {id(page_element): 'result'}
            setattr(page_element, '_PageElement__cached', True)

            self.assertEqual(page_element.__make_object__(page), 'result')

    def test_make_object_not_in_cache_and_class_is_defined(self):
        """Test `__make_object__` method.

        Note:
            Test to get the result by calling `_class` function
            with `page.area` arg.

        """
        with patch(
                'seismograph.ext.selenium.pageobject.Page.area',
                new_callable=PropertyMock) as mock_page_area:
            page = Page()

            page_element = PageElement(dict)

            mock_page_area.return_value = range(100)
            setattr(page_element, '_PageElement__cached', False)
            setattr(page_element, '_PageElement__class', len)

            self.assertEqual(page_element.__make_object__(page), 100)

    def test_get_list_class_defined(self):
        """Test `__get__` method.

        Note:
            Test when `__list_class` specified.

        """
        page_element = PageElement(dict)
        setattr(page_element, '_PageElement__list_class', MagicMock(return_value='result'))
        self.assertEqual(
            page_element.__get__(MagicMock(), MagicMock()), 'result'
        )

    def test_get_list_property_defined(self):
        """Test `__get__` method.

        Note:
            Test when `__property` specified.

        """
        page_element = PageElement(dict)
        setattr(page_element, '_PageElement__property', MagicMock(return_value='result'))
        self.assertEqual(
            page_element.__get__(MagicMock(), MagicMock()), 'result'
        )

    def test_get_list_we_class_defined_and_is_list_not_defined(self):
        """Test `__get__` method.

        Note:
            Test when `__we_class` specified and `__is_list` don't.

        """
        page_element = PageElement(dict)
        setattr(page_element, '_PageElement__we_class', MagicMock(return_value='result'))
        self.assertEqual(
            page_element.__get__(MagicMock(), MagicMock()), 'result'
        )


class PageElementMethodsThrowExceptionTestCase(unittest.TestCase):
    """Tests for `PageElement` class methods in `pageobject.py` module to throw exceptions.

    """

    def setUp(self):
        arg = dict
        self.page_element = PageElement(arg)

    def tearDown(self):
        pass

    # test __getattr__
    def test_getattr(self):
        """Test `__getattr__` method.

        Note:
            This method should throw exception.

        """
        with self.assertRaises(AttributeError):
            self.page_element.getattr('item')

    # test __call__
    def test_call(self):
        """Test `__call__` method.

        Note:
            This method should throw exception.

        """
        with self.assertRaises(TypeError) as context:
            self.page_element()
        self.assertTrue(
            '"{}" is not callable'.format(self.page_element.__class__.__name__) in
            context.exception
        )

    # test __iter__
    def test_iter(self):
        """Test `__iter__` method.

        Note:
            This method should throw exception.

        """
        with self.assertRaises(TypeError) as context:
            iter(self.page_element)
        self.assertTrue(
            '"{}" is not iterable'.format(self.page_element.__class__.__name__) in
            context.exception
        )

    # test __len__
    def test_len(self):
        """Test `__len__` method.

        Note:
            This method should throw exception.

        """
        with self.assertRaises(TypeError) as context:
            len(self.page_element)
        self.assertTrue(
            'object of type "{}" has no len()'.format(self.page_element.__class__.__name__) in
            context.exception
        )

    # test__set__
    def test_set(self):
        """Test `__set__` method.

        Note:
            This method should throw exception.

        """
        # TODO
        pass


# nothing important to test
class PageApiTestCase(unittest.TestCase):
    """Tests for `PageApi` class in `pageobject.py` module.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass


class PageMetaTestCase(unittest.TestCase):
    """Tests for `PageMeta` class in `pageobject.py` module.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_new(self):
        """Test `__new__` method.

        Note:
            Test setting `PageElement` instances in `__dct__`.

        """
        page_element = MagicMock(spec=PageElement)
        page_element.__key__.return_value = 'page_element_key'

        name = 'name'
        bases = (object,)
        dct = {'key': page_element}

        cls_value = PageMeta(name, bases, dct)
        self.assertEqual(cls_value.__dct__, {'page_element_key': 'key'})


class BaseTestCase(unittest.TestCase):
    """Tests for `__Base` class in `pageobject.py` module.

    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getitem(self):
        """Test `__getitem__` method.

        Note:
            # TODO
        """
        # TODO

    def test_getitem_throw_exception(self):
        """Test `__getitem__` method.

        Note:
            This method should throw `KeyError` exception
            when trying to get undefined key.

        """
        with self.assertRaises(KeyError):
            base = _Base()
            base.__getitem__('item')

    def test_getattr(self):
        """Test `__getattr__` method.

        Note:
            Test to return value of `area` attribute by key.

        """
        # TODO
        pass

    def test_area_throw_exception(self):
        """Test `area` method.

        Note:
            This property should always throw `NotImplementedError`.

        """
        base = _Base()
        with self.assertRaises(NotImplementedError):
            base.area

    def test_browser_when_proxy_defined(self):
        """Test `browser` method.

        Note:
            This method should return `browser` attribute of
            `proxy` object which is attribute of the current class
            when `proxy` attribute is specified.

        """
        pass
        # TODO use PropertyMock

    def test_browser_when_proxy_not_defined(self):
        """Test `browser` method.

        Note:
            This method should return `None`
            when `proxy` attribute is not specified.

        """
        base = _Base()
        self.assertIsNone(base.browser)


class PageTestCase(unittest.TestCase):
    """Tests for `Page` class in `pageobject.py` module.

    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_pass_api_class(self):
        """Test `__init__` method.

        Note:
            Test setting `_api` attribute by calling
            `_api_class` function.

        """
        with patch(
                'seismograph.ext.selenium.pageobject.Page.__api_class__',
                new_callable=PropertyMock,
                return_value=MagicMock(return_value='api_class')):
            page = Page()
            self.assertEqual(page.api, 'api_class')

    def test_init_not_pass_api_class(self):
        """Test `__init__` method.

        Note:
            Test setting `_api` attribute to `None` when
            `_api_class` is undefined.

        """
        page = Page()
        self.assertIsNone(page.api)

    def test_area_when_area_not_defined(self):
        """Test `area` method.

        Note:
            This method should return `_proxy` attribute when
            `_area` attribute equals `None`.

        """
        with patch(
                'seismograph.ext.selenium.pageobject.Page._proxy',
                new_callable=PropertyMock,
                return_value=MagicMock(spec=QueryObject)):
            page = Page()
            print(page.area)
            # self.assertEqual(page.area, 'proxy')

    def test_area_when_area_defined_and_area_is_query_object(self):
        """Test `area` method.

        Note:
            This method should always throw exception when
            `_area` attribute is specified and `QueryObject`
            instance.

        """
        pass

    def test_area_when_area_defined_and_area_is_not_query_object(self):
        """Test `area` method.

        Note:
            This method should always throw exception when
            `_area` attribute is specified and it isn't `QueryObject`
            instance.

        """
        with patch(
                'seismograph.ext.selenium.pageobject.Page.__area__',
                new_callable=PropertyMock,
                return_value='area'):
            with self.assertRaises(TypeError) as context:
                page = Page()
                area = page.area
            self.assertTrue('"__area__" can be instance of QueryObject only' in context.exception)

    def test_open_url_path_defined(self):
        pass

    def test_open_url_path_not_defined(self):
        """Test `open` method.

        Note:
            This method should throw exception.

        """
        with self.assertRaises(RuntimeError) as context:
            page = Page()
            page.open()
        self.assertTrue(
            'You should to set "__url_path__" attribute value for usage "show" method' in context.exception
        )

    def test_refresh(self):
        pass


class PageItemTestCase(unittest.TestCase):
    """Tests for `Page` class in `pageobject.py` module.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_we_when_proxy_defined_and_proxy_is_web_element(self):
        """Test `we` method.

        Note:
            If `proxy` attribute is specified and its `is_web_element` attribute equals `True` 
            then this method should return this `proxy` object.

        """
        proxy = MagicMock(spec=ProxyObject)
        setattr(proxy, 'is_web_element', True)

        with patch(
                'seismograph.ext.selenium.pageobject.PageItem._proxy',
                new_callable=PropertyMock,
                return_value=proxy):
            page_item = PageItem()
            self.assertEqual(page_item.we, proxy)

    def test_we_when_proxy_not_defined(self):
        """Test `we` method.

        Note:
            If `proxy` attribute is undefined then this method
            should return `None`.

        """
        page_item = PageItem()
        self.assertIsNone(page_item.we)

    # TO CODE REVIEWER: the tests looks like prevoius tests for Page class
    def test_area_when_area_not_defined(self):
        pass

    def test_area_when_area_defined_and_area_is_query_object(self):
        pass

    def test_area_when_area_defined_and_area_is_not_query_object(self):
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
