import time
import sys
import os
import string
import random
import itertools

sys.path.append(os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                             '..',
                             'file_checker'
                             ]))
import util # noqa
from file_checker.file_checker import FileChecker # noqa
from file_checker.enums import FORMATS # noqa


class TestUtil():
    def test_gen_unique_str(self):
        gen_unique_str = util.gen_unique_str
        u = gen_unique_str('')

        s = ''
        if gen_unique_str(s) in s:
            raise Exception("'{0}' is in '{1}'".format(gen_unique_str(s), s))
        s = u
        if gen_unique_str(s) in s:
            raise Exception("'{0}' is in '{1}'".format(gen_unique_str(s), s))

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            gen_unique_str(u * 256)

        assert time.time() - start < 0.5

    def test_get_first_word(self):
        get_first_word = util.get_first_word

        # asserts
        words = {'': ('', -1, 0),
                 'H': ('H', 0, 1),
                 'HTTP': ('HTTP', 0, 4),
                 'HTTPProtocol': ('HTTP', 0, 4),
                 'HttpProtocol': ('Http', 0, 4),
                 'httpProtocol': ('http', 0, 4),
                 }

        for s, expect in words.items():
            actual = get_first_word(s)
            if expect != actual:
                raise Exception("expect is '{0}', actual is '{1}'".format(
                                expect,
                                actual))

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            get_first_word('U' + 'l' * 255)
            get_first_word('Word' * 64)
            get_first_word('l' * 256)
            get_first_word('U' * 256)
        assert time.time() - start < 5


class TestFileChecker():
    def _gen_random_alphabet_string(self, length=30):
        s = ''
        for i in range(0, length):
            s += random.choice(string.ascii_letters)

        return s

    def _gen_all_possible_pair(self, iterable, beg=0, end=-1):
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

    def test_convert_sep(self):
        fc = FileChecker()

        # boundary
        for sep in self._gen_all_possible_pair(FORMATS['sep']):
            assert '' == fc.convert_sep('', list(sep))
        for s in ['_', '_a', 'a_', 'a_a', '-', '-a', 'a-', 'a-a']:
            assert s == fc.convert_sep(s, [])

        # dash_to_underscore
        assert '_' == fc.convert_sep('-', ['dash_to_underscore'])
        assert '_a' == fc.convert_sep('-a', ['dash_to_underscore'])
        assert 'a_' == fc.convert_sep('a-', ['dash_to_underscore'])
        assert 'a_a' == fc.convert_sep('a-a', ['dash_to_underscore'])

        # underscore_to_dash
        assert '-' == fc.convert_sep('_', ['underscore_to_dash'])
        assert '-a' == fc.convert_sep('_a', ['underscore_to_dash'])
        assert 'a-' == fc.convert_sep('a_', ['underscore_to_dash'])
        assert 'a-a' == fc.convert_sep('a_a', ['underscore_to_dash'])
