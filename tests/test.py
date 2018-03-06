import time
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../file_checker")
from check_name import CheckName # noqa


class TestCheckName():
    def test(self):
        self.test_get_unique_str()
        self.test_get_first_word()
        pass

    def test_get_unique_str(self):
        _get_unique_str = checker._get_unique_str
        u = _get_unique_str('')

        s = ''
        if _get_unique_str(s) in s:
            raise Exception("'{0}' is in '{1}'".format(_get_unique_str(s), s))
        s = u
        if _get_unique_str(s) in s:
            raise Exception("'{0}' is in '{1}'".format(_get_unique_str(s), s))

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            _get_unique_str(u * 256)

        assert time.time() - start < 0.5

    def test_get_first_word(self):
        _get_first_word = checker._get_first_word

        # asserts
        if _get_first_word('') != ('', -1, 0):
            raise Exception("'{0}' != '{1}'".format('',
                            _get_first_word('')[0]))
        if _get_first_word('H') != ('H', 0, 1):
            raise Exception("'{0}' != '{1}'".format('H',
                            _get_first_word('H')[0]))
        if _get_first_word('HTTP') != ('HTTP', 0, 4):
            raise Exception("'{0}' != '{1}'".format('HTTP',
                            _get_first_word('HTTP')[0]))
        if _get_first_word('HTTPProtocol') != ('HTTP', 0, 4):
            raise Exception("'{0}' != '{1}'".format('HTTPProtocol',
                            _get_first_word('HTTPProtocol')[0]))
        if _get_first_word('HttpProtocol') != ('Http', 0, 4):
            raise Exception("'{0}' != '{1}'".format('HttpProtocol',
                            _get_first_word('HttpProtocol')[0]))
        if _get_first_word('httpProtocol') != ('http', 0, 4):
            raise Exception("'{0}' != '{1}'".format('httpProtocol',
                            _get_first_word('httpProtocol')[0]))

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            _get_first_word('Httpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttp')
            _get_first_word('HttpttPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTP')
            _get_first_word('httpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttp')
            _get_first_word('HTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTP')
        assert time.time() - start < 5


if __name__ == '__main__':
    checker = CheckName()
    test = TestCheckName()
    test.test()
