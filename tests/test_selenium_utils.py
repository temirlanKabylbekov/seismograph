# -*- coding: utf-8 -*-

import unittest
from mock import MagicMock, patch

from seismograph.ext.selenium.utils import random_file_name, \
    change_name_from_python_to_html, declare_standard_callback, \
    is_ready_state_complete, re_raise_exc
from seismograph.ext.selenium.proxy import WebDriverProxy
from seismograph.ext.selenium.exceptions import ReRaiseException


class UtilsTestCase(unittest.TestCase):
    """Tests for `utils.py` module.

    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('seismograph.ext.selenium.utils.randint', return_value=500)
    @patch('time.time', return_value=100500.1005)
    def test_random_file_name_check_algorithm(self, mock_time, mock_randint):
        """Test `random_file_name` function.

        Note:
            Test algorithm to generate file name.

        """
        expected_value = int(mock_randint.return_value + mock_time.return_value)
        self.assertEqual(int(random_file_name()), expected_value)

    def test_change_name_from_python_to_html_startswith_underscore(self):
        """Test `change_name_from_python_to_html` function.

        Note:
            Test when passing `name` startswith `_`.

        """
        python_name = '_python_name'
        html_name = change_name_from_python_to_html(python_name)
        self.assertEqual(html_name, 'python-name')

    def test_change_name_from_python_to_html_endswith_underscore(self):
        """Test `change_name_from_python_to_html` function.

        Note:
            Test when passing `name` endswith `_`.

        """
        python_name = 'python_name_'
        html_name = change_name_from_python_to_html(python_name)
        self.assertEqual(html_name, 'python-name')

    def test_change_name_from_python_to_html_contains_underscore(self):
        """Test `change_name_from_python_to_html` function.

        Note:
            Test when passing `name` contains `_` in the middle of part.

        """
        python_name = 'python_name'
        html_name = change_name_from_python_to_html(python_name)
        self.assertEqual(html_name, 'python-name')

    def test_is_ready_state_complete_check_passing_execute_script_arg(self):
        """Test `is_ready_state_complete` function.

        Note:
            Test the argument passing for `execute_script` is
            `return document.readyState`.

        """
        browser = MagicMock(spec=WebDriverProxy)
        is_ready_state_complete(browser)
        browser.execute_script.assert_called_with('return document.readyState')

    def test_declare_standard_callback_pass_not_callable(self):
        """Test `declare_standard_callback` function.

        Note:
            Test when passing not callable arg.

        """
        not_callable_object = 123456
        self.assertEqual(
            declare_standard_callback(not_callable_object),
            not_callable_object
        )

    def test_declare_standard_callback_pass_python_builtin_function(self):
        """Test `declare_standard_callback` function.

        Note:
            Test when passing python builtin function.

        """
        python_builtin_function = len
        self.assertEqual(
            declare_standard_callback(python_builtin_function),
            python_builtin_function
        )

    def test_declare_standard_callback_pass_function_with_many_args(self):
        """Test `declare_standard_callback` function.

        Note:
            Test when passing function which has more than one arg in signature.

        """
        def stub_foo(x, y):
            pass

        with self.assertRaises(TypeError) as context:
            declare_standard_callback(stub_foo)
            self.assertIn('Incorrect signature of function', context.exception)

    def test_declare_standard_callback_pass_function_with_one_arg(self):
        """Test `declare_standard_callback` function.

        Note:
            Test when passing function which has just one arg in signature.

        """
        def stub_foo(x):
            pass

        self.assertEqual(
            declare_standard_callback(stub_foo),
            stub_foo
        )


class ReRaiseRxcTestCase(unittest.TestCase):
    """Tests for `re_raise_exc` function in 'utils.py' module.

    """
    def setUp(self):
        self.base_exception_message = 'base message'
        self.mock_foo = MagicMock()
        self.mock_foo.__name__ = 'name'
        self.mock_foo.side_effect = BaseException(self.base_exception_message)

    def tearDown(self):
        pass

    def test_re_raise_exc_not_specify_message(self):
        """Test `re_raise_exc` function.

        Note:
            Test throwing exception.

        """
        with self.assertRaises(ReRaiseException) as context:
            wrapped = re_raise_exc(self.mock_foo)
            wrapped()
        self.assertIn(self.base_exception_message, context.exception)

    def test_re_raise_exc_specify_message(self):
        """Test `re_raise_exc` function.

        Note:
            Test throwing exception with specified
            message.

        """
        re_raise_exception_message = 're-raise message'
        expected_message = u'{}{}'.format(
            re_raise_exception_message,
            u' (from BaseException: {})'.format(
                self.base_exception_message
                if re_raise_exception_message else
                '(from BaseException)'
            )
        )
        with self.assertRaises(ReRaiseException) as context:
            wrapped = re_raise_exc(self.mock_foo, message=re_raise_exception_message)
            wrapped()
        self.assertIn(expected_message, context.exception)

    def test_re_raise_exc_specify_exception(self):
        """Test `re_raise_exc` function.

        Note:
            Test throwing special type of exception
            passing to this function.

        """
        with self.assertRaises(ValueError) as context:
            wrapped = re_raise_exc(self.mock_foo, exc_cls=ValueError)
            wrapped()
        self.assertIn(self.base_exception_message, context.exception)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
