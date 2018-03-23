import os
import sys
import json
import itertools
import xmltodict
import namanager.tests.helper as helper
from namanager.core import Namanager


class TestNamanager():
    def test_init_settings(self):
        fc = Namanager()
        self.test_load_settings(fc)

        fc.init_settings()

        self.test_properties(fc)

    def test_convert_os_sep_of_str_in_list(self):
        fc = Namanager()
        errors = []
        here = os.path.realpath(os.path.dirname(__file__))

        expect = [os.path.normpath(here)]
        actual = fc._convert_os_sep_of_str_in_list([here])

        helper.append_to_error_if_not_expect_with_msg(
            errors, helper.is_same_disorderly(expect, actual), (
                'Converting OS separator occurs error:'
                'expect: {0}\nactual: {1}'.format(expect, actual)
            ))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_load_settings(self, fc=Namanager()):
        settings = {
            # "CHECK_DIRS": ["123"],
            "ONLY_FILES": ["123"],
            "ONLY_DIRS": ["123"],
            "IGNORE_FILES": ["123"],
            "IGNORE_DIRS": ["123"],
            "FILE_FORMATS": {"LETTER_CASE": "123", "SEP": "123"},
            "DIR_FORMATS": {"LETTER_CASE": "123", "SEP": "123"}
        }

        fc.load_settings(settings)

        assert fc.only_files == ["123"]
        assert fc.only_dirs == ["123"]
        assert fc.ignore_files == ["123"]
        assert fc.ignore_dirs == ["123"]
        assert fc.file_formats == {"LETTER_CASE": "123", "SEP": "123"}
        assert fc.dir_formats == {"LETTER_CASE": "123", "SEP": "123"}
        assert "123" == fc.file_letter_case
        assert "123" == fc.file_sep
        assert "123" == fc.dir_letter_case
        assert "123" == fc.dir_sep

    def test_properties(self, fc=Namanager()):
        assert not fc.error_info
        assert not fc.file_formats
        assert not fc.dir_formats
        assert not fc.only_files
        assert not fc.only_dirs
        assert not fc.ignore_files
        assert not fc.ignore_dirs
        assert not fc.file_sep
        assert not fc.file_letter_case
        assert not fc.dir_sep
        assert not fc.dir_letter_case

    def test_is_string_matching(self):
        fc = Namanager()
        errors = []

        # todo: add more pairs
        expect_pairs = [
            (True, '/root/to/path', ['path']),
            (True, '/root/to/path', ['path$']),
            (True, '/root/to/path', ['/root/to/path']),
            (True, '/root/to/path', ['.*/to/path']),
            (True, '/root/to/path', ['.*/to/pa']),
            (True, '/root/to/path', ['^.*/path$', '^.*/to/path$']),
            (False, '', []),
            (False, 'abc', []),
            (False, '/c/a', ['^/a$']),
            (False, '/root/to/path', ['pa$', '.*/ath$',
                                      '^/path$', '^/to/path$', '^[^/]*path',
                                      '^[^/]*/path', '/root/to/pa$', '.*pa$']),
        ]

        for (expt, string, pattern) in expect_pairs:
            actl = fc._is_string_matching(string, pattern)
            helper.append_to_error_if_not_expect_with_msg(
                errors, expt == actl, (
                    "string:\t{0}\npattern:\t{1}\nexpect: '{0}'\nactl").format(
                        string, pattern, expt, actl))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_convert_walk_to_list(self):
        fc = Namanager()

        actl = fc._convert_walk_to_list(os.path.dirname(sys.executable))

        assert isinstance(actl, list)
        assert isinstance(actl[0], tuple)
        assert isinstance(actl[0][0], str)
        assert isinstance(actl[0][1], list)
        assert isinstance(actl[0][2], list)

    def test_get_root_in_walk(self):
        fc = Namanager()

        expt = os.path.realpath(os.path.dirname(sys.executable))
        walk = [tp for tp in os.walk(expt)]

        actl = fc._get_root_in_walk(walk)

        assert actl == expt

    def test_separate_with_in_out_particular_dir_patterns(self):
        fc = Namanager()
        errors = []
        data = [
            'def',
            'def.xx',
            '/def',
            '^/def',
            'abc/def',
            '/abc/def',
            '^/abc/def',
        ]
        expect_within = [
            '/def',
            '^/def',
            'abc/def',
            '/abc/def',
            '^/abc/def',
        ]
        expect_without = [
            'def',
            'def.xx',
        ]

        actual_within, actual_without = (
            fc._separate_with_in_out_particular_dir_patterns(data))

        helper.append_to_error_if_not_expect_with_msg(
            errors,
            helper.is_same_disorderly(expect_within, actual_within),
            "expect: \n{0}\nactual:\n{1}".format(
                json.dumps(expect_within, indent=4, sort_keys=True),
                json.dumps(actual_within, indent=4, sort_keys=True),
            )
        )
        helper.append_to_error_if_not_expect_with_msg(
            errors,
            helper.is_same_disorderly(expect_without, actual_without),
            "expect: \n{0}\nactual:\n{1}".format(
                json.dumps(expect_without, indent=4, sort_keys=True),
                json.dumps(actual_without, indent=4, sort_keys=True),
            )
        )

    def test_separate_dir_and_file_part_of_patterns(self):
        fc = Namanager()
        errors = []
        data = [
            '/def',
            '^/def',
            'abc/def',
            '/abc/def',
            '^/abc/def',
        ]
        expect_patterns = [
            {
                'dirname': '/',
                'filename': 'def',
            },
            {
                'dirname': '^/',
                'filename': 'def',
            },
            {
                'dirname': 'abc/',
                'filename': 'def',
            },
            {
                'dirname': '/abc/',
                'filename': 'def',
            },
            {
                'dirname': '^/abc/',
                'filename': 'def',
            },
        ]

        actual_patterns = fc._separate_dir_and_file_part_of_patterns(data)

        helper.append_to_error_if_not_expect_with_msg(
            errors,
            helper.is_same_disorderly(expect_patterns, actual_patterns),
            "expect: \n{0}\nactual:\n{1}".format(
                json.dumps(expect_patterns, indent=4, sort_keys=True),
                json.dumps(actual_patterns, indent=4, sort_keys=True),
            )
        )

    def test_include_file_by_match_list_in_walk(self):
        fc = Namanager()
        errors = []
        walk = [
            ('/root/to/path/a', ['a'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/a/a', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/b', ['a'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/b/a', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/c', ['a'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/c/a', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path', ['a', 'b', 'c'], [
                'not.mdfile', 'notmd', 'is.md']),
        ]
        patterns = {
            'test files are particular extension': [
                r'.*\.md$',
            ],
            'test files end with md': [
                r'.*.md$',
            ],
            'test files\' extension include md': [
                r'.*\.md',
            ],
            'test files under particular dir': [
                r'.*/a/is\.md$',
            ],
            'test files under particular dirpath': [
                r'^/a/is\.md$',
            ],
            'test all': [
                r'.*\.md$',
                r'.*.md$',
                r'.*\.md',
                r'.*/a/is\.md$',
                r'^/a/is\.md$',
            ],
        }
        expect_pairs = {
            'test files are particular extension': [
                ('/root/to/path', ['a', 'b', 'c'], ['is.md']),
                ('/root/to/path/a', ['a'], ['is.md']),
                ('/root/to/path/a/a', [], ['is.md']),
                ('/root/to/path/b', ['a'], ['is.md']),
                ('/root/to/path/b/a', [], ['is.md']),
                ('/root/to/path/c', ['a'], ['is.md']),
                ('/root/to/path/c/a', [], ['is.md']),
            ],
            'test files end with md': [
                ('/root/to/path', ['a', 'b', 'c'], ['notmd', 'is.md']),
                ('/root/to/path/a', ['a'], ['notmd', 'is.md']),
                ('/root/to/path/a/a', [], ['notmd', 'is.md']),
                ('/root/to/path/b', ['a'], ['notmd', 'is.md']),
                ('/root/to/path/b/a', [], ['notmd', 'is.md']),
                ('/root/to/path/c', ['a'], ['notmd', 'is.md']),
                ('/root/to/path/c/a', [], ['notmd', 'is.md']),
            ],
            'test files\' extension include md': [
                ('/root/to/path', ['a', 'b', 'c'], ['not.mdfile', 'is.md']),
                ('/root/to/path/a', ['a'], ['not.mdfile', 'is.md']),
                ('/root/to/path/a/a', [], ['not.mdfile', 'is.md']),
                ('/root/to/path/b', ['a'], ['not.mdfile', 'is.md']),
                ('/root/to/path/b/a', [], ['not.mdfile', 'is.md']),
                ('/root/to/path/c', ['a'], ['not.mdfile', 'is.md']),
                ('/root/to/path/c/a', [], ['not.mdfile', 'is.md']),
            ],
            'test files under particular dir': [
                ('/root/to/path/a', ['a'], ['is.md']),
                ('/root/to/path/a/a', [], ['is.md']),
                ('/root/to/path/b/a', [], ['is.md']),
                ('/root/to/path/c/a', [], ['is.md']),
            ],
            'test files under particular dirpath': [
                ('/root/to/path/a', ['a'], ['is.md']),
            ],
            'test all': [
                ('/root/to/path/a', ['a'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/a/a', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/b', ['a'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/b/a', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/c', ['a'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/c/a', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path', ['a', 'b', 'c'], [
                    'not.mdfile', 'notmd', 'is.md']),
            ],
        }

        for description, pattern in patterns.items():
            for p in itertools.permutations(pattern):
                actl = fc._include_file_by_match_list_in_walk(p, walk)
                expt = expect_pairs[description]
                helper.append_to_error_if_not_expect_with_msg(
                    errors, helper.is_same_disorderly(expt, actl), (
                        "description:\t{0}\npattern:\t{1}"
                        "\nexpect: '{2}'\nactl: '{3}'").format(
                            description,
                            p,
                            json.dumps(expt, indent=4, sort_keys=True),
                            json.dumps(actl, indent=4, sort_keys=True)))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_exclude_file_by_match_list_in_walk(self):
        fc = Namanager()
        errors = []
        walk = [
            ('/root/to/path', ['a', 'b', 'c'], [
                'not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/a', ['a'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/a/a', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/b', ['a'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/b/a', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/c', ['a'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/c/a', [], ['not.mdfile', 'notmd', 'is.md']),
        ]
        classified_patterns = {
            'test files are particular extension': [
                r'.*\.md$',
            ],
            'test files end with md': [
                r'.*.md$',
            ],
            'test files\' extension include md': [
                r'.*\.md',
            ],
            'test files under particular dir': [
                r'.*/a/is\.md$',
            ],
            'test files under particular dirpath': [
                r'^/a/is\.md$',
            ],
            'test all': [
                r'.*\.md$',
                r'.*.md$',
                r'.*\.md',
                r'.*/a/is\.md$',
                r'^/a/is\.md$',
            ],
        }
        expect_pairs = {
            'test files are particular extension': [
                ('/root/to/path', ['a', 'b', 'c'], ['notmd', 'not.mdfile']),
                ('/root/to/path/a', ['a'], ['notmd', 'not.mdfile']),
                ('/root/to/path/a/a', [], ['notmd', 'not.mdfile']),
                ('/root/to/path/b', ['a'], ['notmd', 'not.mdfile']),
                ('/root/to/path/b/a', [], ['notmd', 'not.mdfile']),
                ('/root/to/path/c', ['a'], ['notmd', 'not.mdfile']),
                ('/root/to/path/c/a', [], ['notmd', 'not.mdfile']),
            ],
            'test files end with md': [
                ('/root/to/path', ['a', 'b', 'c'], ['not.mdfile']),
                ('/root/to/path/a', ['a'], ['not.mdfile']),
                ('/root/to/path/a/a', [], ['not.mdfile']),
                ('/root/to/path/b', ['a'], ['not.mdfile']),
                ('/root/to/path/b/a', [], ['not.mdfile']),
                ('/root/to/path/c', ['a'], ['not.mdfile']),
                ('/root/to/path/c/a', [], ['not.mdfile']),
            ],
            'test files\' extension include md': [
                ('/root/to/path', ['a', 'b', 'c'], ['notmd']),
                ('/root/to/path/a', ['a'], ['notmd']),
                ('/root/to/path/a/a', [], ['notmd']),
                ('/root/to/path/b', ['a'], ['notmd']),
                ('/root/to/path/b/a', [], ['notmd']),
                ('/root/to/path/c', ['a'], ['notmd']),
                ('/root/to/path/c/a', [], ['notmd']),
            ],
            'test files under particular dir': [
                ('/root/to/path', ['a', 'b', 'c'], [
                    'not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/a', ['a'], ['not.mdfile', 'notmd']),
                ('/root/to/path/a/a', [], ['not.mdfile', 'notmd']),
                ('/root/to/path/b', ['a'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/b/a', [], ['not.mdfile', 'notmd']),
                ('/root/to/path/c', ['a'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/c/a', [], ['not.mdfile', 'notmd']),
            ],
            'test files under particular dirpath': [
                ('/root/to/path', ['a', 'b', 'c'], [
                    'not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/a', ['a'], ['not.mdfile', 'notmd']),
                ('/root/to/path/a/a', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/b', ['a'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/b/a', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/c', ['a'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/c/a', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test all': [
            ],
        }

        for description, patterns in classified_patterns.items():
            for pattern in itertools.permutations(patterns):
                actl = fc._exclude_file_by_match_list_in_walk(pattern, walk)
                expt = expect_pairs[description]
                helper.append_to_error_if_not_expect_with_msg(
                    errors, helper.is_same_disorderly(expt, actl), (
                        "description:\t{0}\npattern:\t{1}"
                        "\nexpect: '{2}'\nactl: '{3}'").format(
                            description,
                            pattern,
                            json.dumps(expt, indent=4, sort_keys=True),
                            json.dumps(actl, indent=4, sort_keys=True)))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_include_dir_by_match_list_in_walk(self):
        fc = Namanager()
        errors = []
        walk = [
            ('/root/to/path', ['aa', 'ba', 'ca'], [
                'not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/aa', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/aa/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ba', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ba/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ca', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ca/aa', [], ['not.mdfile', 'notmd', 'is.md']),
        ]
        patterns = {
            'test particular dir': [
                r'a',
            ],
            'test particular dir it starts with ba': [
                r'/ba[^/]*',
            ],
            'test dir under particular dir': [
                r'.*/aa$',
            ],
            'test dir in particular dirpath': [
                r'^/ba/aa$',
            ],
            'test all': [
                r'a',
                r'/ba[^/]*',
                r'.*/aa$',
                r'^/ba/aa$',
            ],
        }
        expect_pairs = {
            'test particular dir': [
                ('/root/to/path/aa', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/aa/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test particular dir it starts with ba': [
                ('/root/to/path/ba', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test dir under particular dir': [
                ('/root/to/path/aa', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/aa/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test dir in particular dirpath': [
                ('/root/to/path/ba/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test all': [
                ('/root/to/path/aa', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/aa/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
        }

        for description, pattern in patterns.items():
            for p in itertools.permutations(pattern):
                actl = fc._include_dir_by_match_list_in_walk(p, walk)
                expt = expect_pairs[description]
                helper.append_to_error_if_not_expect_with_msg(
                    errors, helper.is_same_disorderly(expt, actl), (
                        "description:\t{0}\npattern:\t{1}"
                        "\nexpect: '{2}'\nactl: '{3}'").format(
                            description,
                            p,
                            json.dumps(expt, indent=4, sort_keys=True),
                            json.dumps(actl, indent=4, sort_keys=True)))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_exclude_dir_by_match_list_in_walk(self):
        fc = Namanager()
        errors = []
        walk = [
            ('/root/to/path', ['aa', 'ba', 'ca'], [
                'not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/aa', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/aa/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ba', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ba/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ca', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
            ('/root/to/path/ca/aa', [], ['not.mdfile', 'notmd', 'is.md']),
        ]
        patterns = {
            'test particular dir': [
                r'a',
            ],
            'test particular dir it starts with ba': [
                r'/ba[^/]*',
            ],
            'test dir under particular dir': [
                r'.*/aa$',
            ],
            'test dir in particular dirpath': [
                r'^/ba/aa$',
            ],
            'test all': [
                r'a',
                r'/ba[^/]*',
                r'.*/aa$',
                r'^/ba/aa$',
            ],
        }
        expect_pairs = {
            'test particular dir': [
                ('/root/to/path', ['aa', 'ba', 'ca'], [
                    'not.mdfile', 'notmd', 'is.md']),
            ],
            'test particular dir it starts with ba': [
                ('/root/to/path', ['aa', 'ba', 'ca'], [
                    'not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/aa', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/aa/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test dir under particular dir': [
                ('/root/to/path', ['aa', 'ba', 'ca'], [
                    'not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test dir in particular dirpath': [
                ('/root/to/path', ['aa', 'ba', 'ca'], [
                    'not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/aa', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/aa/aa', [], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ba', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca', ['aa'], ['not.mdfile', 'notmd', 'is.md']),
                ('/root/to/path/ca/aa', [], ['not.mdfile', 'notmd', 'is.md']),
            ],
            'test all': [
                ('/root/to/path', ['aa', 'ba', 'ca'], [
                    'not.mdfile', 'notmd', 'is.md']),
            ],
        }

        for description, pattern in patterns.items():
            for p in itertools.permutations(pattern):
                actl = fc._exclude_dir_by_match_list_in_walk(p, walk)
                expt = expect_pairs[description]
                helper.append_to_error_if_not_expect_with_msg(
                    errors, helper.is_same_disorderly(expt, actl), (
                        "description:\t{0}\npattern:\t{1}"
                        "\nexpect: '{2}'\nactl: '{3}'").format(
                            description,
                            p,
                            json.dumps(expt, indent=4, sort_keys=True),
                            json.dumps(actl, indent=4, sort_keys=True)))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_get_file_list(self):
        pass

    def test_get_dir_list(self):
        pass

    def test_check_file(self):
        # only test it can works
        fc = Namanager()
        errors = []
        etc = {
            "CHECK_DIRS": [
                os.path.realpath(
                    os.path.join(os.path.dirname(__file__), '..', '..')),
            ],
            "ONLY_FILES": [],
            "ONLY_DIRS": [],
            "IGNORE_FILES": [],
            "IGNORE_DIRS": [],
            "FILE_FORMATS": {
                "LETTER_CASE": "pascal_case",
                "SEP": "dash_to_underscore",
            },
            "DIR_FORMATS": {
                "LETTER_CASE": "pascal_case",
                "SEP": "dash_to_underscore",
            },
        }

        fc.load_settings(etc)
        fc.check_file(etc['CHECK_DIRS'][0])

        for f in fc.get_dict():
            expect = f['filename']['expect']
            actual = f['filename']['actual']
            helper.append_to_error_if_not_expect_with_msg(
                errors, len(expect) == len(actual), (
                    "expect: {0}\nactual: {1}\nin: {2}".format(
                        expect, actual, f['dirpath'])))
        assert errors == [], Exception(helper.get_error_string(errors))

    def test_check_dir(self):
        pass

    def test_check(self):
        pass

    def test_get_xml_json_dict(self):
        fc = Namanager()
        data = [
            {"_id": "5aa7e7247d6d91ca300e1fb3","index": 0,"guid": "319cb0fe-29b9-4d60-9fde-4e82aee9bc16","booleans": [True, False],"lists": [[True], [False]],"numbers": {'1':{'1':1}, '2':{'2':2}, '3':{'3':3}},"list": [213, 3],"isActive": False,"balance": "$2,803.51","picture": "http://placehold.it/32x32","age": 31,"eyeColor": "brown","name": "Esperanza Weeks","gender": "female","company": "EZENTIA","email": "esperanzaweeks@ezentia.com","phone": "+1 (930) 533-3206","address": "653 Division Avenue, Tilleda, Ohio, 5025","about": "Duis laborum dolor veniam aliqua nostrud velit excepteur qui. Est consectetur incididunt amet nulla pariatur. Do non consequat in occaecat quis esse incididunt. Dolore eu adipisicing esse ad quis et nisi ut ad. Adipisicing amet magna deserunt aliquip nulla laboris cupidatat velit qui ipsum deserunt. Nulla cupidatat eu nisi eu duis nostrud duis sint culpa consectetur fugiat do tempor laboris.","registered": "2014-11-26T08:32:11 -08:00","latitude": 83.870374,"longitude": 165.0311,"tags": ["non","laboris","sit","pariatur","enim","magna","qui"],"friends": [{"id": 0,"name": "Claudine Butler"},{"id": 1,"name": "Tate Potts"},{"id": 2,"name": "Clark Franco"}],"greeting": "Hello, Esperanza Weeks! You have 6 unread messages.","favoriteFruit": "apple"}, # noqa
        ]

        for d in data:
            fc._error_info = d
            # get dict
            helper.is_same_disorderly(d, fc.get_dict())
            # get json
            helper.is_same_disorderly(
                d, json.dumps(fc.get_json(), indent=4, sort_keys=True))
            # get xml
            helper.is_same_disorderly(
                d, json.dumps(xmltodict.parse(fc.get_xml()),
                              indent=4,
                              sort_keys=True))
