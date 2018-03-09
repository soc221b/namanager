import time
import sys
import os
import string
import random
import itertools

sys.path.append(os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                             '..',
                             'src'
                             ]))
import util # noqa
from file_checker import FileChecker # noqa
from enums import FORMATS # noqa


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


class TestUtil():
    def test_gen_unique_str(self):
        gen_unique_str = util.gen_unique_str
        errors = []
        u = gen_unique_str('')

        s = ''
        if gen_unique_str(s) in s:
            errors.push(["'{0}' is in '{1}'".format(gen_unique_str(s), s)])
        s = u
        if gen_unique_str(s) in s:
            errors.push(["'{0}' is in '{1}'".format(gen_unique_str(s), s)])

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            gen_unique_str(u * 256)

        if time.time() - start > 0.5:
            errors.push(['The algorithm is not efficient.'])

        if errors:
            raise Exception(get_error_string(errors))

    def test_get_first_word(self):
        get_first_word = util.get_first_word
        errors = []

        # asserts
        words = {'': ('', -1, 0),
                 'H': ('H', 0, 1),
                 'HTTP': ('HTTP', 0, 4),
                 'HTTPProtocol': ('HTTP', 0, 4),
                 'HttpProtocol': ('Http', 0, 4),
                 'httpProtocol': ('http', 0, 4),
                 '*H': ('H', 1, 2),
                 '*HTTP': ('HTTP', 1, 5),
                 '*HTTPProtocol': ('HTTP', 1, 5),
                 '*HttpProtocol': ('Http', 1, 5),
                 '*httpProtocol': ('http', 1, 5),
                 'H*': ('H', 0, 1),
                 'HTTP*': ('HTTP', 0, 4),
                 'HTTP*Protocol': ('HTTP', 0, 4),
                 'Http*Protocol': ('Http', 0, 4),
                 'http*Protocol': ('http', 0, 4),
                 }

        for s, expect in words.items():
            actual = get_first_word(s)
            if expect != actual:
                errors.push(["expect is '{0}', actual is '{1}'".format(expect,
                             actual)])

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            get_first_word('U' + 'l' * 255)
            get_first_word('Word' * 64)
            get_first_word('l' * 256)
            get_first_word('U' * 256)
        if time.time() - start > 5:
            errors.push(['The algorithm is not efficient.'])

        if errors:
            raise Exception(get_error_string(errors))

    def convert_words_to_case(self, words, case):
        exp = []
        if case == 'lower_case':
            for w in words:
                exp += [w.lower()]
        if case == 'upper_case':
            for w in words:
                exp += [w.upper()]
        if case == 'camel_case' or case == 'pascal_case':
            for w in words:
                exp += [w.lower()]
            for i, w in enumerate(exp):
                if w:
                    w = w[0].upper() + w[1:]
                exp[i] = w
            if case == 'camel_case':
                first_alphabet = 0
                for i, w in enumerate(exp):
                    first_alphabet = 0
                    while (first_alphabet < len(w) and
                           not w[first_alphabet].isalpha()):
                        first_alphabet += 1
                    if first_alphabet < len(w):
                        exp[i] = w[:first_alphabet] + \
                                 w[first_alphabet].lower() + \
                                 w[first_alphabet + 1:]
                        break
        return exp

    def test_get_words(self):
        get_words = util.get_words
        errors = []

        test_data = {'lower_case': [
                        '',
                        '.',
                        '....',
                        'http_error&response.for.request-of?soap',
                        '.http_error&response.for.request-of?soap',
                        'http_error&response.for.request-of?soap.',
                        '.http_error&response.for.request-of?soap.',
                        '....http_error&response.for.request-of?soap',
                        'http_error&response.for.request-of?soap....',
                        '....http_error&response.for.request-of?soap....',
                        ],
                     'upper_case': [
                        '',
                        '.',
                        '....',
                        'HTTP_ERROR&RESPONSE.FOR.REQUEST-OF?SOAP',
                        '.HTTP_ERROR&RESPONSE.FOR.REQUEST-OF?SOAP',
                        'HTTP_ERROR&RESPONSE.FOR.REQUEST-OF?SOAP.',
                        '.HTTP_ERROR&RESPONSE.FOR.REQUEST-OF?SOAP.',
                        '....HTTP_ERROR&RESPONSE.FOR.REQUEST-OF?SOAP',
                        'HTTP_ERROR&RESPONSE.FOR.REQUEST-OF?SOAP....',
                        '....HTTP_ERROR&RESPONSE.FOR.REQUEST-OF?SOAP....',
                        ],
                     'camel_case': [
                        '',
                        '.',
                        '....',
                        'http_Error&Response.For.Request-Of?Soap',
                        '.http_Error&Response.For.Request-Of?Soap',
                        'http_Error&Response.For.Request-Of?Soap.',
                        '.http_Error&Response.For.Request-Of?Soap.',
                        '....http_Error&Response.For.Request-Of?Soap',
                        'http_Error&Response.For.Request-Of?Soap....',
                        '....http_Error&Response.For.Request-Of?Soap....',
                        'httpErrorResponseForRequestOfSoap',
                        '.httpErrorResponseForRequestOfSoap',
                        'httpErrorResponseForRequestOfSoap.',
                        '.httpErrorResponseForRequestOfSoap.',
                        '....httpErrorResponseForRequestOfSoap',
                        'httpErrorResponseForRequestOfSoap....',
                        '....httpErrorResponseForRequestOfSoap....',
                        ],
                     'pascal_case': [
                        '',
                        '.',
                        '....',
                        'Http_Error&Response.For.Request-Of?Soap',
                        '.Http_Error&Response.For.Request-Of?Soap',
                        'Http_Error&Response.For.Request-Of?Soap.',
                        '.Http_Error&Response.For.Request-Of?Soap.',
                        '....Http_Error&Response.For.Request-Of?Soap',
                        'Http_Error&Response.For.Request-Of?Soap....',
                        '....Http_Error&Response.For.Request-Of?Soap....',
                        'HttpErrorResponseForRequestOfSoap',
                        '.HttpErrorResponseForRequestOfSoap',
                        'HttpErrorResponseForRequestOfSoap.',
                        '.HttpErrorResponseForRequestOfSoap.',
                        '....HttpErrorResponseForRequestOfSoap',
                        'HttpErrorResponseForRequestOfSoap....',
                        '....HttpErrorResponseForRequestOfSoap....',
                        ]
                     }

        words_only_alphabet = [
            [],
            [],
            [],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
            ['http', 'error', 'response', 'for', 'request', 'of', 'soap'],
        ]

        words_non_alphabet = [
            [],
            ['.'],
            ['....'],
            ['http', '_', 'error', '&', 'response', '.', 'for', '.', 'request',
             '-', 'of', '?', 'soap'],
            ['.', 'http', '_', 'error', '&', 'response', '.', 'for', '.',
             'request', '-', 'of', '?', 'soap'],
            ['http', '_', 'error', '&', 'response', '.', 'for', '.', 'request',
             '-', 'of', '?', 'soap', '.'],
            ['.', 'http', '_', 'error', '&', 'response', '.', 'for', '.',
             'request', '-', 'of', '?', 'soap', '.'],
            ['....', 'http', '_', 'error', '&', 'response', '.', 'for', '.',
             'request', '-', 'of', '?', 'soap'],
            ['http', '_', 'error', '&', 'response', '.', 'for', '.', 'request',
             '-', 'of', '?', 'soap', '....'],
            ['....', 'http', '_', 'error', '&', 'response', '.', 'for', '.',
             'request', '-', 'of', '?', 'soap', '....'],
            ['Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap'],
            ['.', 'Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap'],
            ['Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap', '.'],
            ['.', 'Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap',
             '.'],
            ['....', 'Http', 'Error', 'Response', 'For', 'Request', 'Of',
             'Soap'],
            ['Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap',
             '....'],
            ['....', 'Http', 'Error', 'Response', 'For', 'Request', 'Of',
             'Soap', '....'],
        ]

        for include_non_alphabet in [True, False]:
            if include_non_alphabet:
                with_or_not = "with"
            else:
                with_or_not = "without"

            for case, sentences in test_data.items():
                for i, sent in enumerate(sentences):
                    if include_non_alphabet:
                        words = words_non_alphabet[i]
                    else:
                        words = words_only_alphabet[i]

                    for sep in ['.', '*', '?', '1', '/', "\\", '^', '$']:
                        # substitute escape signs
                        exp = []
                        for e in words:
                            exp += [e.replace(r'.', sep)]
                        exp = self.convert_words_to_case(exp, case)
                        act = get_words(sent.replace('.', sep),
                                        include_non_alphabet)

                        if act != exp:
                            errors.push([("The '{0}' {1} non-alphabet in {2}\n"
                                          "expect: {3}\nactual: {4}").format(
                                          sent.replace(r'.', sep), with_or_not,
                                          case, exp, act)])

        if errors:
            raise Exception(get_error_string(errors))


class TestFileChecker():
    def test_convert_sep(self):
        fc = FileChecker()
        errors = []

        # boundary
        for sep in gen_all_possible_pair(FORMATS['sep']):
            act = fc.convert_sep('', list(sep))
            if '' != act:
                errors.push(["'' != {0}".format(act)])
        for s in ['_', '_a', 'a_', 'a_a', '-', '-a', 'a-', 'a-a']:
            act = fc.convert_sep(s, [])
            if s != act:
                errors.push(["{0} != {1}".format(s, act)])

        # dash_to_underscore
        act = fc.convert_sep('-', ['dash_to_underscore'])
        if '_' != act:
            errors.push(["expect '_' != actual '{0}'".format(act)])
        act = fc.convert_sep('-a', ['dash_to_underscore'])
        if '_a' != act:
            errors.push(["expect '_a' != actual '{0}'".format(act)])
        act = fc.convert_sep('a-', ['dash_to_underscore'])
        if 'a_' != act:
            errors.push(["expect 'a_' != actual '{0}'".format(act)])
        act = fc.convert_sep('a-a', ['dash_to_underscore'])
        if 'a_a' != act:
            errors.push(["expect 'a_a' != actual '{0}'".format(act)])

        # underscore_to_dash
        act = fc.convert_sep('_', ['underscore_to_dash'])
        if '-' != act:
            errors.push(["expect '-' != actual '{0}'".format(act)])
        act = fc.convert_sep('_a', ['underscore_to_dash'])
        if '-a' != act:
            errors.push(["expect '-a' != actual '{0}'".format(act)])
        act = fc.convert_sep('a_', ['underscore_to_dash'])
        if 'a-' != act:
            errors.push(["expect 'a-' != actual '{0}'".format(act)])
        act = fc.convert_sep('a_a', ['underscore_to_dash'])
        if 'a-a' != act:
            errors.push(["expect 'a-a' != actual '{0}'".format(act)])

        if errors:
            raise Exception(get_error_string(errors))
