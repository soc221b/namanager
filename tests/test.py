import time
import sys
import os

sys.path.append(
    os.path.dirname(os.path.realpath(__file__)) + "/../file_checker")
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
        if get_first_word('') != ('', -1, 0):
            raise Exception("'{0}' != '{1}'".format('',
                            get_first_word('')[0]))
        if get_first_word('H') != ('H', 0, 1):
            raise Exception("'{0}' != '{1}'".format('H',
                            get_first_word('H')[0]))
        if get_first_word('HTTP') != ('HTTP', 0, 4):
            raise Exception("'{0}' != '{1}'".format('HTTP',
                            get_first_word('HTTP')[0]))
        if get_first_word('HTTPProtocol') != ('HTTP', 0, 4):
            raise Exception("'{0}' != '{1}'".format('HTTPProtocol',
                            get_first_word('HTTPProtocol')[0]))
        if get_first_word('HttpProtocol') != ('Http', 0, 4):
            raise Exception("'{0}' != '{1}'".format('HttpProtocol',
                            get_first_word('HttpProtocol')[0]))
        if get_first_word('httpProtocol') != ('http', 0, 4):
            raise Exception("'{0}' != '{1}'".format('httpProtocol',
                            get_first_word('httpProtocol')[0]))

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            get_first_word('Httpttpttpttpttppttpttpttpttpttppttpttpttpttpttp \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttptt')
            get_first_word('HttpttPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTP \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTT')
            get_first_word('httpttpttpttpttppttpttpttpttpttppttpttpttpttpttp \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttpttppttpttpttpttpttppttpttpttpttptt \
                            ppttpttpttpttptt')
            get_first_word('HTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTP \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTTPPTTPTTPTTPTTPTT \
                            PPTTPTTPTTPTTPTT')
        assert time.time() - start < 5
