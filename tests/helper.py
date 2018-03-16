import random
import itertools
import string
import collections


def get_error_string(errors):
    err_str = '\n'
    for error in errors:
        err_str += error + '\n\n'
    return err_str


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


def _is_same(a, b):
    if type(a) != type(b):
        return False

    if isinstance(a, collections.Iterable):
        if len(a) != len(b):
            return False

    if isinstance(a, dict):
        for k, v in a.items():
            if (k not in b or
               not _is_same(a[k], b[k])):
                return False

    elif isinstance_of_types(a, [set, tuple]):
        for v in a:
            if v not in b:
                return False

    elif isinstance_of_types(a, [list]):
        try:
            a.sort()
            b.sort()
        except TypeError as e:
            pass

        for index, v in enumerate(a):
            if v not in b:
                return False
            if isinstance_of_types(v, [list, tuple, set, dict]):
                return _is_same(a[index], b[index])
    else:
        return a == b

    return True


def is_same(a, b):
    return _is_same(a, b) and _is_same(b, a)


def _dump_space(string, spaces):
    s = spaces
    while s != 0:
        string += " "
        s -= 1
    return string


def _determine_last(dump_callback, string, json_, col_start_at_=0):
    return dump_callback(string, json_, col_start_at_)


def _dump_dict(string, dict_, col_start_at_=0):
    # warning: cannot use int as key of dict
    string += "{\n"

    for index, (key, value) in enumerate(dict_.items()):
        string = _dump_space(string, col_start_at_)
        string += '"' + str(key) + '"' + ": "

        if isinstance(value, list) and len(value) > 0:
            string = _determine_last(
                _dump_list, string, value, col_start_at_ + 4)

        elif isinstance(value, dict) and len(value) > 0:
            string = _determine_last(
                _dump_dict, string, value, col_start_at_ + 4)

        else:
            if isinstance(value, str):
                string += '"' + value + '"'
            elif isinstance(value, bool):
                if value:
                    string += "true"
                else:
                    string += "false"
            else:
                string += str(value)

        if index != len(dict_) - 1:
            string += ","
        string += "\n"

    string = _dump_space(string, col_start_at_ - 4)
    string += "}"
    return string


def _dump_list(string, list_, col_start_at_=0):
    string += "[\n"

    for index, value in enumerate(list_):
        string = _dump_space(string, col_start_at_)

        if isinstance(value, list) and len(value) > 0:
            string = _determine_last(
                _dump_list, string, value, col_start_at_ + 4)

        elif isinstance(value, dict) and len(value) > 0:
            string = _determine_last(
                _dump_dict, string, value, col_start_at_ + 4)

        else:
            if isinstance(value, str):
                string += '"' + value + '"'
            elif isinstance(value, bool):
                if value:
                    string += "true"
                else:
                    string += "false"
            else:
                string += str(value)

        if index != len(list_) - 1:
            string += ","
        string += "\n"

    string = _dump_space(string, col_start_at_ - 4)
    string += "]"
    return string


def format_dump(json_, col_start_at_=4):
    string = ''

    if isinstance(json_, list):
        if json_:
            string = _determine_last(_dump_list, string, json_, col_start_at_)

    elif isinstance(json_, dict):
        if json_:
            string = _determine_last(_dump_dict, string, json_, col_start_at_)

    return string
