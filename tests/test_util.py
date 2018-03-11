import time
import sys
import os

sys.path.append(os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                             '..',
                             'src'
                             ]))
import helper # noqa
import util # noqa
from enums import FORMATS # noqa


class TestUtil():
    def test_gen_unique_str(self):
        gen_unique_str = util.gen_unique_str
        errors = []
        u = gen_unique_str('')

        s = ''
        if gen_unique_str(s) in s:
            errors.append("'{0}' is in '{1}'".format(gen_unique_str(s), s))
        s = u
        if gen_unique_str(s) in s:
            errors.append("'{0}' is in '{1}'".format(gen_unique_str(s), s))

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            gen_unique_str(u * 256)

        if time.time() - start > 0.5:
            errors.append('The algorithm is not efficient.')

        assert errors == [], Exception(helper.get_error_string(errors))

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
                errors.append("expect is '{0}', actual is '{1}'".format(expect,
                              actual))

        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            get_first_word('U' + 'l' * 255)
            get_first_word('Word' * 64)
            get_first_word('l' * 256)
            get_first_word('U' * 256)
        if time.time() - start > 5:
            errors.append('The algorithm is not efficient.')

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_get_words(self):
        get_words = util.get_words
        convert_words_to_case = util.convert_words_to_case
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

        words_only = [
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

        words_with_other_char = [
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

        for include_non_letter in [True, False]:
            if include_non_letter:
                with_or_not = "with"
            else:
                with_or_not = "without"

            for case, sentences in test_data.items():
                for i, sent in enumerate(sentences):
                    if include_non_letter:
                        words = words_with_other_char[i]
                    else:
                        words = words_only[i]

                    for sep in ['.', '*', '?', '1', '/', "\\", '^', '$']:
                        # substitute escape signs
                        expt = []
                        for e in words:
                            expt += [e.replace(r'.', sep)]
                        expt = convert_words_to_case(expt, case)
                        actl = get_words(sent.replace('.', sep),
                                         include_non_letter)

                        if actl != expt:
                            errors.append(("The '{0}' {1} non-alphabet in {2}"
                                           "\nexpect: {3}"
                                           "\nactual: {4}").format(
                                               sent.replace(r'.', sep),
                                               with_or_not, case, expt,
                                               actl))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_convert_sentence_to_case(self):
        """
        This test is assumed that
        convert_words will be called indirectly by convert_sentence
        """

        convert_sentence_to_case = util.convert_sentence_to_case
        errors = []

        # boundary
        actl = convert_sentence_to_case('', [])
        if '' != actl:
            errors.append("'' != '{0}'".format(actl))
        for case in helper.gen_all_possible_pair(FORMATS['letter_case']):
            if '' != convert_sentence_to_case('', list(case)):
                errors.append("'' != {0}".format(
                              convert_sentence_to_case('', list(case))))

        # with any separator
        expect = {'lower_case': 'http_error&response*for.request-of?soap',
                  'upper_case': 'HTTP_ERROR&RESPONSE*FOR.REQUEST-OF?SOAP',
                  'camel_case': 'http_Error&Response*For.Request-Of?Soap',
                  'pascal_case': 'Http_Error&Response*For.Request-Of?Soap',
                  }

        strings = ['http_error&response*for.request-of?soap',
                   'HTTP_ERROR&RESPONSE*FOR.REQUEST-OF?SOAP',
                   'http_Error&Response*For.Request-Of?Soap',
                   'Http_Error&Response*For.Request-Of?Soap',
                   ]

        for case in helper.gen_all_possible_pair(FORMATS['letter_case']):
            for s in strings:
                expt = expect[case[-1]]
                actl = convert_sentence_to_case(s, case[-1])
                if expt != actl:
                    errors.append("In format: {0} within any separator \
                                  \nexpect: {1} !=\nactual: {2}".format(
                                  case, expt, actl))

        # without any separator
        # httperrorresponseforrequestofsoap
        expect = {'lower_case': 'httperrorresponseforrequestofsoap',
                  'upper_case': 'HTTPERRORRESPONSEFORREQUESTOFSOAP',
                  'camel_case': 'httpErrorResponseForRequestOfSoap',
                  'pascal_case': 'HttpErrorResponseForRequestOfSoap',
                  }

        strings = ['httpErrorResponseForRequestOfSoap',
                   'HttpErrorResponseForRequestOfSoap',
                   ]

        for case in helper.gen_all_possible_pair(FORMATS['letter_case']):
            for s in strings:
                expt = expect[case[-1]]
                actl = convert_sentence_to_case(s, case[-1])
                if expt != actl:
                    errors.append("In format: {0} without any separator \
                                  \nexpect: {1} !=\nactual: {2}".format(
                                  case, expt, actl))
        assert errors == [], Exception(helper.get_error_string(errors))
