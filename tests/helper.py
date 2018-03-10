import random
import itertools
import string


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


def gen_all_possible_pair(iterable, beg=0, end=-1):
    """
    :param iterable:
    :type iterable: list, str or iterable types
    :return: tuple -
    """
    if end == -1:
        end = len(iterable)
    res = []
    for i in range(beg, end):
        for comb in itertools.combinations(iterable, i + 1):
            res += itertools.permutations(comb)
    return res
