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
            act = fc.convert_sep('', list(sep))
            if '' != act:
                errors.append("'' != {0}".format(act))
        for s in ['_', '_a', 'a_', 'a_a', '-', '-a', 'a-', 'a-a']:
            act = fc.convert_sep(s, [])
            if s != act:
                errors.append("{0} != {1}".format(s, act))

        # dash_to_underscore
        act = fc.convert_sep('-', ['dash_to_underscore'])
        if '_' != act:
            errors.append("expect '_' != actual '{0}'".format(act))
        act = fc.convert_sep('-a', ['dash_to_underscore'])
        if '_a' != act:
            errors.append("expect '_a' != actual '{0}'".format(act))
        act = fc.convert_sep('a-', ['dash_to_underscore'])
        if 'a_' != act:
            errors.append("expect 'a_' != actual '{0}'".format(act))
        act = fc.convert_sep('a-a', ['dash_to_underscore'])
        if 'a_a' != act:
            errors.append("expect 'a_a' != actual '{0}'".format(act))

        # underscore_to_dash
        act = fc.convert_sep('_', ['underscore_to_dash'])
        if '-' != act:
            errors.append("expect '-' != actual '{0}'".format(act))
        act = fc.convert_sep('_a', ['underscore_to_dash'])
        if '-a' != act:
            errors.append("expect '-a' != actual '{0}'".format(act))
        act = fc.convert_sep('a_', ['underscore_to_dash'])
        if 'a-' != act:
            errors.append("expect 'a-' != actual '{0}'".format(act))
        act = fc.convert_sep('a_a', ['underscore_to_dash'])
        if 'a-a' != act:
            errors.append("expect 'a-a' != actual '{0}'".format(act))

        assert errors == [], Exception(util.get_error_string(errors))
