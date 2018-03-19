import random
import itertools
import string
import collections
import json


def get_error_string(errors):
    err_str = '\n'
    for error in errors:
        err_str += error + '\n\n'
    return err_str


def append_to_error_if_not_expect_with_msg(error, expect, msg):
    if not expect:  # pragma: no cover
        error.append(msg)


def gen_random_alphabet_string(length=30):
    s = ''
    for i in range(0, length):
        s += random.choice(string.ascii_letters)

    return s


def gen_all_possible_pair(iterable, beg=0, end=None):
    """
    :param iterable:
    :type iterable: list, str or iterable types
    :return: tuple -
    """
    if end is None:
        end = len(iterable)
    res = []
    for i in range(beg, end):
        for comb in itertools.combinations(iterable, i + 1):
            res += itertools.permutations(comb)
    return res


def isinstance_of_types(value_, type_):
    if (isinstance(type_, list) or
       isinstance(type_, set)):
        for t in type_:
            if isinstance_of_types(value_, t):
                return True
    else:
        return isinstance(value_, type_)

    return False


def _is_same(a, b, convert_unicode=True):
    if type(a) != type(b):  # pragma: no cover
        if convert_unicode:
            try:
                a.encode('UTF-8')
                b.encode('UTF-8')
            except Exception:
                return False
        else:
            return False

    if isinstance(a, collections.Iterable):
        if len(a) != len(b):
            return False

    if isinstance(a, dict):
        for k, v in a.items():
            if (k not in b or
               not _is_same(a[k], b[k], convert_unicode)):
                return False

    elif isinstance_of_types(a, [set, tuple]):
        for v in a:
            if v not in b:
                return False

    elif isinstance_of_types(a, [list]):
        try:
            a.sort()
            b.sort()
        except TypeError:  # pragma: no cover
            pass

        for index, v in enumerate(a):
            if v not in b:
                return False
            if isinstance_of_types(v, [list, tuple, set, dict]):
                return _is_same(a[index], b[index], convert_unicode)
    else:
        return a == b

    return True


def is_same(a, b, convert_unicode=True):
    return _is_same(a, b, convert_unicode) and _is_same(b, a, convert_unicode)


def format_dump(json_, col_start_at_=4):
    return json.dumps(json_, indent=4, sort_keys=True)
