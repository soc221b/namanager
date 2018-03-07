import time
import sys
import os

sys.path.append(os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                             '..',
                             'file_checker'
                             ]))
import util # noqa


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
            get_first_word('Word' + 'U' * 63)
            get_first_word('l' * 256)
            get_first_word('U' * 256)
        assert time.time() - start < 5
