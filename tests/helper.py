import os
import tempfile
import random
import itertools
import string
import collections


def mktemps(count, **kwargs):  # pragma: no cover
    # haven't been tested
    filenames = []

    for i in range(count):
        filenames.append(mktemp(**kwargs))

    return filenames


def mkdtemps(count, **kwargs):  # pragma: no cover
    # haven't been tested
    dirnames = []

    for i in range(count):
        dirnames.append(mkdtemp(**kwargs))

    return dirnames


def mkdtemps_recur(dir_count=0, recur_count=0, **kwargs):  # pragma: no cover
    # haven't been tested
    file_count = kwargs.get('file_count', 0)
    prefix = kwargs.get('prefix', '')

    dirnames = mkdtemps(dir_count, **kwargs)
    filenames = []
    for dn in dirnames:
        filenames.extend(mktemps(file_count, root=dn,
                         prefix=prefix))

    pathnames = dirnames + filenames
    if recur_count > 0:
        for dn in dirnames[:]:
            pathnames.extend(mkdtemps_recur(dir_count,
                                            recur_count - 1,
                                            file_count=file_count,
                                            root=dn,
                                            prefix=prefix))

    return pathnames


def mktemp(**kwargs):  # pragma: no cover
    # haven't been tested
    root = kwargs.get('root', os.path.dirname(__file__))
    prefix = kwargs.get('prefix', '')
    dirname = os.path.realpath(root)
    tmpfile = tempfile.mkstemp(dir=dirname, prefix=prefix)[1]

    return os.path.realpath(tmpfile)


def mkdtemp(**kwargs):  # pragma: no cover
    # haven't been tested
    root = kwargs.get('root', os.path.dirname(__file__))
    prefix = kwargs.get('prefix', '')

    dirname = os.path.realpath(root)
    tmpdir = tempfile.mkdtemp(dir=dirname, prefix=prefix)

    return os.path.realpath(tmpdir)


def rm_paths(paths):
    paths.sort(key=lambda p: len(p.split(os.sep)), reverse=True)

    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
    for path in paths:
        if os.path.isdir(path):
            os.rmdir(path)


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


def is_in_tuple(x, t):
    for i in t:
        if i is x:
            return True
    return False


def is_equal(a, b):
    return ((a == b and
            (not is_in_tuple(a, (None, True, False))) and
             (not is_in_tuple(b, (None, True, False)))) or
            (a is None and b is None) or
            (a is True and b is True) or
            (a is False and b is False))


def _is_same_disorderly_list(a, b, convert_unicode=True):
    try:
        a.sort()
        b.sort()
    except TypeError:  # pragma: no cover
        pass

    for index, v in enumerate(a):
        if isinstance(v, (list, tuple, set, dict)):
            return _is_same_disorderly(a[index], b[index], convert_unicode)
        elif v not in b:
            return False
    return True


def _is_same_disorderly_tuple(a, b, convert_unicode=True):
    """
    tuple cannot be sorted
    we can classify elements by type and then test each
    """
    a_classified_list = classify_different_type_element(a)
    b_classified_list = classify_different_type_element(b)

    # test each
    for i in a_classified_list:
        same_index = -1
        for index, j in enumerate(b_classified_list):
            try:
                i.sort()
                j.sort()
            except Exception:  # pragma: no cover
                pass
            # if type of i and j are same
            if isinstance(i[0], type(j[0])):
                same_index = index
                if not _is_same_disorderly(i, j, convert_unicode):
                    return False
        # remove tested elements
        if same_index != -1:
            del b_classified_list[same_index]
    return True


def classify_different_type_element(tuple_):
    classified_list = []

    for element in tuple_:
        appended = False
        for list_ in classified_list:
            if isinstance(element, type(list_[0])):
                list_.append(element)
                appended = True
        if not appended:
            classified_list.append([element])

    return classified_list


def _is_same_disorderly_dict(a, b, convert_unicode=True):
    for k, v in a.items():
        if k in b:
            if isinstance(v, (list, tuple, set, dict)):
                if not _is_same_disorderly(a[k], b[k], convert_unicode):
                    return False
            elif not is_equal(v, b[k]):
                return False
        else:
            return False
    return True


def _is_same_disorderly_set(a, b, convert_unicode=True):
    return _is_same_disorderly(list(a), list(b), convert_unicode)


def _is_same_disorderly_check_len(a, b):
    if isinstance(a, collections.Iterable):
        if len(a) != len(b):
            return False
    return True


def _is_same_disorderly_check_type(a, b, convert_unicode=True):
    same = True
    if type(a) != type(b):
        if convert_unicode:
            try:
                # Backward compatibility
                # python2.7 u's' != 's'
                a = a.encode('UTF-8')
                b = b.encode('UTF-8')
            except Exception:
                same = False
        else:
            same = False

    return same, a, b


def _is_same_disorderly(a, b, convert_unicode=True):
    # test variables are same or contain same elements without order
    same, a, b = _is_same_disorderly_check_type(a, b, convert_unicode)
    if not same:
        return False
    if not _is_same_disorderly_check_len(a, b):
        return False

    if isinstance(a, dict):
        return _is_same_disorderly_dict(a, b, convert_unicode)
    elif isinstance(a, set):
        return _is_same_disorderly_set(a, b, convert_unicode)
    elif isinstance(a, tuple):
        return _is_same_disorderly_tuple(a, b, convert_unicode)
    elif isinstance(a, list):
        return _is_same_disorderly_list(a, b, convert_unicode)
    else:
        return a == b


def is_same_disorderly(a, b, convert_unicode=True):
    return (_is_same_disorderly(a, b, convert_unicode) and
            _is_same_disorderly(b, a, convert_unicode))


def get_all_type_values_of_json():
    # Types of json/python mapping:
    # int, float, True, False, None, dict, list, (long), (str), (unicode)
    type_values = (1, 2, 3.4, 4.5, True, False, None)
    dict_values = ()
    list_values = ()
    # Compatibility
    try:  # pragma: no cover
        # python2, long
        type_values = (long(5),) + type_values  # noqa: F821
        type_values = (long(6),) + type_values  # noqa: F821
        # python2, unicode
        type_values = (u'abc',) + type_values
        type_values = (u'bcd',) + type_values
    except Exception:  # pragma: no cover
        # python3, str
        type_values = ('abc',) + type_values
        type_values = ('bcd',) + type_values
    for i in type_values:
        for j in type_values:
            try:
                dict_values += ({i: j},)
            except Exception:  # pragma: no cover
                pass
    for i in type_values:
        for j in type_values:
            try:
                list_values += ([j],)
            except Exception:  # pragma: no cover
                pass
    type_values += dict_values
    type_values += list_values

    return type_values
