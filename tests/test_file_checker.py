import os
import sys
sys.path.append(os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                             '..',
                             'src'
                             ]))
import helper # noqa
import util # noqa
from file_checker import FileChecker # noqa
from enums import FORMATS # noqa


class TestFileChecker():
    def test_convert_sep(self):
        fc = FileChecker()
        errors = []

        # boundary
        for sep in helper.gen_all_possible_pair(FORMATS['sep']):
            actl = fc.convert_sep('', list(sep))
            if '' != actl:
                errors.append("'' != {0}".format(actl))
        for s in ['_', '_a', 'a_', 'a_a', '-', '-a', 'a-', 'a-a']:
            actl = fc.convert_sep(s, [])
            if s != actl:
                errors.append("{0} != {1}".format(s, actl))

        # dash_to_underscore
        actl = fc.convert_sep('-', ['dash_to_underscore'])
        if '_' != actl:
            errors.append("expect '_' != actlual '{0}'".format(actl))
        actl = fc.convert_sep('-a', ['dash_to_underscore'])
        if '_a' != actl:
            errors.append("expect '_a' != actlual '{0}'".format(actl))
        actl = fc.convert_sep('a-', ['dash_to_underscore'])
        if 'a_' != actl:
            errors.append("expect 'a_' != actlual '{0}'".format(actl))
        actl = fc.convert_sep('a-a', ['dash_to_underscore'])
        if 'a_a' != actl:
            errors.append("expect 'a_a' != actlual '{0}'".format(actl))

        # underscore_to_dash
        actl = fc.convert_sep('_', ['underscore_to_dash'])
        if '-' != actl:
            errors.append("expect '-' != actlual '{0}'".format(actl))
        actl = fc.convert_sep('_a', ['underscore_to_dash'])
        if '-a' != actl:
            errors.append("expect '-a' != actlual '{0}'".format(actl))
        actl = fc.convert_sep('a_', ['underscore_to_dash'])
        if 'a-' != actl:
            errors.append("expect 'a-' != actlual '{0}'".format(actl))
        actl = fc.convert_sep('a_a', ['underscore_to_dash'])
        if 'a-a' != actl:
            errors.append("expect 'a-a' != actlual '{0}'".format(actl))

        assert errors == [], Exception(util.get_error_string(errors))
