# -*- coding: utf-8 -*-
# @Time    : 2023/8/31 16:02:16
# @Author  : Pane Li
# @File    : in_expect.py
"""
in_expect

"""
import datetime
import os
import typing


class expect:
    def __init__(self, value, args=None, kwargs=None):
        self._value = value
        self._args = args
        self._kwargs = kwargs

    @staticmethod
    def __dict_flatten(in_dict, separator=":", dict_out=None, parent_key=None) -> dict:
        """ 平铺字典

        :param in_dict: 输入的字典
        :param separator: 连接符号
        :param dict_out:
        :param parent_key:
        :return: dict
        """
        if dict_out is None:
            dict_out = {}

        for k, v in in_dict.items():
            k = f"{parent_key}{separator}{k}" if parent_key else k
            if isinstance(v, dict) and v:
                expect.__dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
                continue

            dict_out[k] = v

        return dict_out

    @staticmethod
    def __dict_to_list(in_dict, list_out=None) -> list:
        """  将字典里面的所有key 和 value 转换成列表

        :param in_dict: 输入的字典
        :param list_out:

        :return: list
        """
        if list_out is None:
            list_out = []
        if in_dict is not None:
            for k, v in in_dict.items():
                list_out.append(k)
                if isinstance(v, dict):
                    expect.__dict_to_list(in_dict=v, list_out=list_out)
                    continue
                list_out.append(v)

        return list_out

    @staticmethod
    def __dict_in(expect_dict: dict, contain: dict) -> None:
        """验证字典包含关系

        :param expect_dict: dict {key: value}
        :param contain: dict,  支持${value} 表达式判断
        :return: AssertionError
        """
        if expect_dict and contain:
            contain_flatten = expect.__dict_flatten(contain)  # 平铺字典
            expect_dict_flatten = expect.__dict_flatten(expect_dict)  # 平铺字典
            for contain_item, contain_value in contain_flatten.items():
                if contain_item in expect_dict_flatten.keys():
                    value = expect_dict_flatten.get(contain_item)
                    assert value == contain_value, f'expect {expect_dict} to contain "{contain_item}":"{contain_value}"'
                else:
                    # 找出与后面相匹配的key
                    reg_item = [expect_item for expect_item in expect_dict_flatten.keys() if
                                expect_item.endswith(contain_item)]
                    if reg_item:
                        for item in reg_item:
                            value = expect_dict_flatten.get(item)
                            if value == contain_value:
                                break
                        else:
                            raise AssertionError(f'expect {expect_dict} to contain "{contain_item}":"{contain_value}"')
                    else:
                        raise AssertionError(f'expect {expect_dict} to contain keys {contain_item} ')

    @staticmethod
    def __dict_not_in(expect_dict: dict, contain: dict) -> None:
        """验证字典包含关系

        :param expect_dict: dict {key: value}
        :param contain: dict,  支持${value} 表达式判断
        :return: AssertionError
        """
        if expect_dict and contain:
            contain_flatten = expect.__dict_flatten(contain)  # 平铺字典
            expect_dict_flatten = expect.__dict_flatten(expect_dict)  # 平铺字典
            for contain_item, contain_value in contain_flatten.items():
                if contain_item in expect_dict_flatten.keys():
                    value = expect_dict_flatten.get(contain_item)
                    assert value != contain_value, f'expect {expect_dict} not contain "{contain_item}":"{contain_value}"'
                else:
                    # 找出与后面相匹配的key
                    reg_item = [expect_item for expect_item in expect_dict_flatten.keys() if
                                expect_item.endswith(contain_item)]
                    if reg_item:
                        for item in reg_item:
                            value = expect_dict_flatten.get(item)
                            if value == contain_value:
                                raise AssertionError(
                                    f'expect {expect_dict} not contain "{contain_item}":"{contain_value}"')

    @staticmethod
    def __contain(expect_value: list or tuple or set, arg):
        """

        :param expect_value:
        :param arg:
        :return:
        """
        result = False
        if isinstance(arg, dict):
            for value_one in expect_value:
                if isinstance(value_one, dict):  # 如果是字典
                    try:
                        expect.__dict_in(value_one, arg)  # 先判断在不在，在就退出，不在就往下走
                        result = True
                    except AssertionError:
                        pass
                elif isinstance(value_one, (list, tuple, set)):
                    result = expect.__contain(value_one, arg)
                if result:
                    break
        elif isinstance(arg, (tuple, list, set)):  # 如果是集合就一个一个的找
            for arg_ in arg:
                result = expect.__contain(expect_value, arg_)
                if not result:
                    break
        else:
            if arg not in expect_value:
                for value_one in expect_value:
                    if isinstance(value_one, (list, tuple, set)):
                        result = expect.__contain(value_one, arg)
                    if result:
                        break
            else:
                result = True
        return result

    @staticmethod
    def __not_contain(expect_value: list or tuple or set, arg):
        """

        :param expect_value:
        :param arg:
        :return:
        """
        result = True  # 假设不包含为True， 包含了为False， 所以只要检测到False 就退出
        if isinstance(arg, dict):
            for value_one in expect_value:
                if isinstance(value_one, dict):  # 如果是字典
                    try:
                        expect.__dict_in(value_one, arg)  # 先判断在不在，在就退出，不在就往下走
                        result = False
                    except AssertionError:
                        pass
                elif isinstance(value_one, (list, tuple, set)):
                    result = expect.__not_contain(value_one, arg)
                if not result:
                    break
        elif isinstance(arg, (tuple, list, set)):  # 如果是集合就一个一个的找
            for arg_ in arg:
                result = expect.__not_contain(expect_value, arg_)
                if not result:
                    break
        else:
            if arg not in expect_value:
                for value_one in expect_value:
                    if isinstance(value_one, (list, tuple, set)):
                        result = expect.__not_contain(value_one, arg)
                    if not result:
                        break
            else:
                result = False
        return result

    def is_eq(self, *args):
        """Value is equal， 非严格相同， 只要值相等即可，可以是列表也可以是元组和字典等类型
           ex: expect(1).is_eq(1).is_ne(2)
           a = [1, 2, 3]
           expect(a).is_eq([1, 2, 3])
           a = {"a": 1, "b": 2}
           expect(a).is_eq({"a": 1, "b": 2})
        """
        try:
            for arg in args:
                assert self._value == arg, f'expect <{self._value}> is equal <{arg}>'
        except TypeError:
            raise
        return self

    def is_ne(self, *args):
        """Value is not equal
           ex: expect(1).is_ne(2).is_eq(1)
        """
        try:
            for arg in args:
                assert self._value != arg, f'expect <{self._value}> is not equal <{arg}>'
        except TypeError:
            raise
        return self

    def is_lt(self, *args):
        """Value is less than
           ex: expect(1).is_lt(2).is_gt(0)
        """
        try:
            for arg in args:
                assert self._value < arg, f'expect <{self._value}> is less than <{arg}>'
        except TypeError:
            raise
        return self

    def is_gt(self, *args):
        """Value is more than
           ex: expect(2).is_gt(1).is_lt(3)
        """
        try:
            for arg in args:
                assert self._value > arg, f'expect <{self._value}> is more than <{arg}>'
        except TypeError:
            raise
        return self

    def is_le(self, *args):
        """Value is less than or equal
           ex: expect(1).is_le(1).is_ge(1)
        """
        try:
            for arg in args:
                assert self._value <= arg, f'expect <{self._value}> is less than or equal <{arg}>'
        except TypeError:
            raise
        return self

    def is_ge(self, *args):
        """Value is more than or equal
           ex: expect(1).is_ge(1).is_le(1)
        """
        try:
            for arg in args:
                assert self._value >= arg, f'expect <{self._value}> is more than or equal <{arg}>'
        except TypeError:
            raise
        return self

    def is_be(self, *args):
        """Value is the same, 严格相同
           ex: expect(1).is_be(1).is_not_be(2), expect('1').is_be('1').is_not_be('2')
        """
        try:
            for arg in args:
                assert self._value is arg, f'expect <{self._value}> is be {arg}'
        except TypeError:
            raise
        return self

    def is_be_false(self):
        """Value is False  False|0|''|[]|{}|None|()"""
        try:
            assert not self._value, f'expect <{self._value}> is be False'
        except TypeError:
            raise
        return self

    def is_be_true(self):
        """Value is True  True|1|'1'|[1]|{"a": 1}|(1, )"""
        try:
            assert self._value, f'expect <{self._value}> is be True'
        except TypeError:
            raise
        return self

    def is_not_be(self, *args):
        """Value is not the same
           ex: expect(1).is_not_be(2).is_be(1), expect('1').is_not_be('2').is_be('1')
        """
        try:
            for arg in args:
                assert self._value is not arg, f'expect <{self._value}> is not be <{arg}>'
        except TypeError:
            raise
        return self

    def to_be_empty(self):
        """Value is empty  |''|[]|{}|()"""
        try:
            assert len(self._value) == 0, f'expect <{self._value}> to be empty'
        except TypeError:
            raise
        return self

    def to_contain(self, *args, flags=0):
        """Value contains
        支持字符串
        value = 'Hello, World'
        expect(value).to_contain('Hello', re.compile('Hello'), 'World', 'Hello, World')
        expect(value).to_contain(r'hello', flags=re.IGNORECASE)  flags 只有在匹配正则表达式时才有效，但不能是re.compile
        value = b'Hello, World'
        expect(value).to_contain(b'Hello', re.compile(b'Hello'), b'World', b'Hello, World')
        expect(value).to_contain(rb'hello', flags=re.IGNORECASE)
        value = [1, 'Hello, World', [1, 2, [4, 5]], {'a': 1, 'b': {'c': 2}}, b'hello', None, True]
        expect(value).to_contain('Hello, World', 1, [1, 2, [4, 5]], {'a': 1, 'b': {'c': 2}}, b'hello', None, True)
        expect(value).to_contain(1, 2, [1, 2], [4, 5], 4)
        expect(value).to_contain({'a': 1}, {'b': {"c": 2}}, {'c': 2})
        value = {"k1": '123', 'k2': {"k2-1": None, "k2-2": {"k3": 1}}, 'k4': [123]}
        expect(value).to_contain({'k2': {"k2-1": None}}, {'k2-2': {"k3": 1}}, {'k3': 1}, {"k1": '123'})
        expect(value).to_contain('k2-2', 'k2-1', 'k3', 'k1')
        expect(value).to_contain(None, 1, [123])
        """
        if self._value:
            for arg in args:
                if isinstance(self._value, (str, bytes)):
                    if arg:
                        try:
                            assert re.search(arg, self._value, flags), f'expect <{self._value}> to contain <{arg}>'
                        except TypeError:
                            raise TypeError(f'expect <{self._value}> to contain <{arg}> type error')
                    else:
                        raise ValueError(f'{arg} is False')
                elif isinstance(self._value, (list, tuple, set)):
                    assert expect.__contain(self._value, arg), f'expect <{self._value}> to contain <{arg}>'
                elif isinstance(self._value, dict):
                    if isinstance(arg, dict):
                        expect.__dict_in(self._value, arg)
                    else:
                        try:
                            assert arg in self.__dict_to_list(
                                self._value), f'expect <{self._value}> to contain <{arg}>'
                        except TypeError:
                            raise TypeError(f'expect <{self._value}> to contain <{arg}> type error')
                else:
                    raise TypeError(f'not support value type')
        else:
            raise ValueError(f'value is False')
        return self

    def to_not_contain(self, *args, flags=0):
        """Value not contains
        和 to_contain 成反比
        """
        if self._value:
            for arg in args:
                if isinstance(self._value, (str, bytes)):
                    if arg:
                        try:
                            assert not re.search(arg, self._value, flags), f'expect <{self._value}> not contain <{arg}>'
                        except TypeError:
                            pass
                    else:
                        raise ValueError(f'{arg} is False')
                elif isinstance(self._value, (list, tuple, set)):
                    assert expect.__not_contain(self._value, arg), f'expect <{self._value}> not contain <{arg}>'
                elif isinstance(self._value, dict):
                    if isinstance(arg, dict):
                        expect.__dict_not_in(self._value, arg)
                    elif isinstance(arg, (list, tuple, set)):
                        self.to_not_contain(*arg, flags=flags)
                    else:
                        try:
                            assert arg not in self.__dict_to_list(
                                self._value), f'expect <{self._value}> not contain <{arg}>'
                        except TypeError:
                            pass
                else:
                    raise TypeError(f'not support value type')
        else:
            raise ValueError(f'value is False')
        return self

    def is_in(self, *args, flags=0):
        """同 to_contain， 只是反转了下角色

        :param args:
        :param flags:
        :return:
        """
        if self._value:
            for arg in args:
                try:
                    expect(arg).to_contain(self._value, flags=flags)
                except AssertionError:
                    raise AssertionError(f'expect <{self._value}> is in <{arg}>')
                except TypeError:
                    raise TypeError(f'expect <{self._value}> is in <{arg}> type error')
        else:
            raise ValueError(f'value is False')
        return self

    def is_not_in(self, *args, flags=0):
        """
        同 to_not_contain， 只是反转了下角色
        :param args:
        :param flags:
        :return:
        """
        if self._value:
            for arg in args:
                try:
                    expect(arg).to_not_contain(self._value, flags=flags)
                except AssertionError:
                    raise AssertionError(f'expect <{self._value}> is not in <{arg}>')
                except TypeError:
                    raise TypeError(f'expect <{self._value}> is not in <{arg}> type error')
        else:
            raise ValueError(f'value is False')
        return self

    def is_length(self, *args):
        """Array or string has length
           ex: expect('Hello, World').is_length(12)
           expect([1, 2, 3]).is_length(3)
        """
        try:
            for arg in args:
                assert len(self._value) == arg, f'expect <{self._value}> is length <{arg}>'
        except TypeError:
            raise
        return self

    def to_have_property(self, arg: str, arg_value: typing.Any):
        """dict has a property  or list contain dict has a property
            ex:
            value = {a: {b: [42]}, c: True}
            expect(value).to_have_property('a.b', [42])
            expect(value).to_have_property('a.b[0]', 42)
            value = [{a: 1}, {a: 2}]
            expect(value).to_have_property('[0].a', 1)
        """
        try:
            keys = arg.split('.')
            expression = 'self._value'
            for key in keys:
                if key.startswith('['):
                    expression += f'{key}'
                else:
                    key_ = key.split('[', 1)[0]
                    try:
                        key_list = key.split('[', 1)[1]
                        expression += f'.get("{key_}")[{key_list}'
                    except IndexError:
                        expression += f'.get("{key_}")'
            now_value = eval(expression, {'self': self})
            assert now_value == arg_value, f'expect <{self._value}> to have property <{arg}> is <{arg_value}>'
        except TypeError:
            raise
        return self

    def to_match(self, *args, flags=0):
        """string value matches a regular expression
           ex:
           expect('Hello, World').to_match(r'Hello')
           expect('Hello, World').to_match(re.compile(r'^Hello.*'))
        """
        import re
        try:
            for arg in args:
                assert re.match(arg, self._value, flags), f'expect <{self._value}> to match <{arg}>'
        except TypeError:
            raise
        return self

    def to_not_match(self, *args, flags=0):
        """string value matches a regular expression
           ex:
           expect('Hello, World').to_match(r'Hello')
           expect('Hello, World').to_match(re.compile(r'^Hello.*'))
        """
        import re
        try:
            for arg in args:
                assert not re.match(arg, self._value, flags), f'expect <{self._value}> to not match <{arg}>'
        except TypeError:
            raise
        return self

    def to_be_instance_of(self, arg):
        """Value is instance of
            ex:
            value = [1, 2, 3]
            expect(value).to_be_instance_of(list)
        """
        try:
            assert isinstance(self._value, arg), f'expect <{self._value}> to be instance of <{arg}>'
        except TypeError:
            raise
        return self

    def exists(self):
        """Asserts val is a path and that it exists.

        Examples:
            Usage::

                expect('myfile.txt').exists()
                expect('mydir').exists()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** exist
        """
        if not isinstance(self._value, str):
            raise TypeError(f'{self._value} is not a path')
        if not os.path.exists(self._value):
            raise AssertionError(f'expect <%s> to exist, but was not found.' % self._value)
        return self

    def is_before(self, *args, format='%Y-%m-%dT%H:%M:%SZ'):
        """Asserts val is a date and is before other date.
               Args:
                   *args: the other date, expected to be before val
                   format: the format of the date, defaults to '%Y-%m-%dT%H:%M:%SZ'
               Examples:
                   Usage::
                       import datetime
                       today = datetime.datetime.now()
                       yesterday = today - datetime.timedelta(days=1)
                       expect(yesterday).is_before(today)
               Returns:
                   AssertionBuilder: returns this instance to chain to the next assertion

               Raises:
                   AssertionError: if val is **not** before the given date

               """
        if type(format) is str:
            val = datetime.datetime.strptime(self._value, format)
            args = [datetime.datetime.strptime(arg, format) for arg in args]
        else:
            raise TypeError('format must be str, but was type <%s>' % type(format).__name__)
        for other in args:
            if val >= other:
                raise AssertionError(f'expect <{self._value.strftime(format)}> to be before <{other.strftime(format)}>')
        return self

    def is_after(self, *args, format='%Y-%m-%dT%H:%M:%SZ'):
        """Asserts val is a date and is after other date.
                       Args:
                           *args: the other date, expected to be after val
                           format: the format of the date, defaults to '%Y-%m-%dT%H:%M:%SZ'
                       Examples:
                           Usage::
                               import datetime
                               today = datetime.datetime.now()
                               yesterday = today - datetime.timedelta(days=1)
                               expect(today).is_after(yesterday)
                       Returns:
                           AssertionBuilder: returns this instance to chain to the next assertion

                       Raises:
                           AssertionError: if val is **not** before the given date

                       """
        if type(format) is str:
            val = datetime.datetime.strptime(self._value, format)
            args = [datetime.datetime.strptime(arg, format) for arg in args]
        else:
            raise TypeError('format must be str, but was type <%s>' % type(format).__name__)
        for other in args:
            if val <= other:
                raise AssertionError(f'expect <{self._value.strftime(format)}> to be after <{other.strftime(format)}>')
        return self

    def is_equal_to_ignore_milliseconds(self, *args, format='%Y-%m-%dT%H:%M:%SZ'):
        """Asserts value is a date and is equal to other date to the second.
                Args:
                    args: the other date, expected to be equal to the second
                    format:  the format of the date, defaults to '%Y-%m-%dT%H:%M:%SZ'
                Examples:
                    Usage::
                        import datetime
                        d1 = datetime.datetime(2020, 1, 2, 3, 4, 5, 6)       # 2020-01-02 03:04:05.000006
                        d2 = datetime.datetime(2020, 1, 2, 3, 4, 5, 777777)  # 2020-01-02 03:04:05.777777

                        expect(d1).is_equal_to_ignore_milliseconds(d2)
                Returns:
                    AssertionBuilder: returns this instance to chain to the next assertion

                Raises:
                    AssertionError: if val is **not** equal to the given date to the second
                """
        if type(format) is str:
            val = datetime.datetime.strptime(self._value, format)
            args = [datetime.datetime.strptime(arg, format) for arg in args]
        else:
            raise TypeError('format must be str, but was type <%s>' % type(format).__name__)
        for other in args:
            if val.date() != other.date() or val.hour != other.hour or val.minute != other.minute or val.second != other.second:
                raise AssertionError(
                    f'expect <{self._value.strftime(format)}> to be equal to <{other.strftime(format)}>')
        return self

    def is_equal_to_ignore_seconds(self, *args, format='%Y-%m-%dT%H:%M:%SZ'):
        """Asserts value is a date and is equal to other date to the minute.
                Args:
                    args: the other date, expected to be equal to the minute
                    format: the format of the date, defaults to '%Y-%m-%dT%H:%M:%SZ'
                Examples:
                    Usage::
                        import datetime

                        d1 = datetime.datetime(2020, 1, 2, 3, 4, 5)   # 2020-01-02 03:04:05
                        d2 = datetime.datetime(2020, 1, 2, 3, 4, 55)  # 2020-01-02 03:04:55
                        expect(d1).is_equal_to_ignore_seconds(d2)
                Returns:
                    AssertionBuilder: returns this instance to chain to the next assertion
                Raises:
                    AssertionError: if val is **not** equal to the given date to the minute
                """
        if type(format) is str:
            val = datetime.datetime.strptime(self._value, format)
            args = [datetime.datetime.strptime(arg, format) for arg in args]
        else:
            raise TypeError('format must be str, but was type <%s>' % type(format).__name__)
        for other in args:
            if val.date() != other.date() or val.hour != other.hour or val.minute != other.minute:
                raise AssertionError(
                    f'expect <{self._value.strftime(format)}> to be equal to <{other.strftime(format)}>')
        return self

    def is_equal_to_ignore_time(self, *args, format='%Y-%m-%dT%H:%M:%SZ'):
        """Asserts value is a date and is equal to other date ignoring time.
                Args:
                    args: the other date, expected to be equal ignoring time
                    format: the format of the date, defaults to '%Y-%m-%dT%H:%M:%SZ'
                Examples:
                    Usage::
                        import datetime

                        d1 = datetime.datetime(2020, 1, 2, 3, 4, 5)     # 2020-01-02 03:04:05
                        d2 = datetime.datetime(2020, 1, 2, 13, 44, 55)  # 2020-01-02 13:44:55
                        expect(d1).is_equal_to_ignore_time(d2)
                Returns:
                    AssertionBuilder: returns this instance to chain to the next assertion
                Raises:
                    AssertionError: if val is **not** equal to the given date ignoring time
                """
        if type(format) is str:
            val = datetime.datetime.strptime(self._value, format)
            args = [datetime.datetime.strptime(arg, format) for arg in args]
        else:
            raise TypeError('format must be str, but was type <%s>' % type(format).__name__)
        for other in args:
            if val.date() != other.date():
                raise AssertionError(
                    f'expect <{self._value.strftime(format)}> to be equal to <{other.strftime(format)}>')
        return self

    def is_increase_seconds(self, increase: int, format='%Y-%m-%dT%H:%M:%SZ'):
        """Asserts value is a date and is increase to other date.
                Args:
                    increase: 递增的时间，单位秒
                    format: the format of the date, defaults to '%Y-%m-%dT%H:%M:%SZ'
        """
        if type(self._value) not in (list, tuple, set):
            raise TypeError(f'{self._value} is not a list or tuple or set')
        else:
            val = [datetime.datetime.strptime(arg, format) for arg in self._value]
            if len(val) >= 2:
                t0 = val[0]
                for value_ in val[1:]:
                    assert (value_ - t0).seconds == increase, \
                        f'expect <{value_.strftime(format)}> is increase <{increase}> seconds error'
                    t0 = value_

    def is_decrease_seconds(self, increase: int, format='%Y-%m-%dT%H:%M:%SZ'):
        """Asserts value is a date and is decrease to other date.
                Args:
                    increase: 递减的时间，单位秒
                    format: the format of the date, defaults to '%Y-%m-%dT%H:%M:%SZ'
        """
        if type(self._value) not in (list, tuple, set):
            raise TypeError(f'{self._value} is not a list or tuple or set')
        else:
            val = [datetime.datetime.strptime(arg, format) for arg in self._value]
            if len(val) >= 2:
                t0 = val[0]
                for value_ in val[1:]:
                    assert (t0 - value_).seconds == increase, \
                        f'expect <{value_.strftime(format)}> is decrease <{increase}> seconds error'
                    t0 = value_


class raises:

    def __init__(self, expected_exception, match=None):
        if not issubclass(expected_exception, BaseException):
            raise TypeError(f"expected_exception must be classes, not {expected_exception.__name__}")
        if not isinstance(match, (str, typing.Pattern, type(None))):
            raise TypeError(f"match must be str or typing.Pattern")
        self.expected_exception = expected_exception
        self.match = match

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            if not issubclass(exc_type, self.expected_exception):
                return False
            if self.match is not None:
                if isinstance(self.match, str):
                    if self.match not in str(exc_value):
                        return False
                else:
                    if not self.match.search(str(exc_value)):
                        return False
            # 返回True表示异常已被处理，否则异常将继续传播
            return True
        else:
            raise Exception(f"DID NOT RAISE {self.expected_exception.__name__}")


if __name__ == '__main__':
    import re

    value = ['2023-08-31T16:02:10Z', '2023-08-31T16:02:15Z', '2023-08-31T16:02:21Z']
    expect(value).is_increase_seconds(5)
    # expect(value).is_in('Hello', 'Hello, World')
