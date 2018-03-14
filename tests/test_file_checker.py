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
    def test_is_string_matching(self):
        fc = FileChecker()
        errors = []

        # todo: add more pairs
        expect_pairs = [
            (False, "", []),
        ]

        for (expt, string, pattern) in expect_pairs:
            actl = fc.is_string_matching(string, pattern)
            if expt != actl:
                errors.append(("string:\t{0}\npattern:\t{1}"
                               "\nexpect: '{0}' != \nactl").format(
                               string, pattern, expt, actl))

        assert errors == [], Exception(util.get_error_string(errors))
