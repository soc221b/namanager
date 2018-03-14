import os
import re
import json
import dicttoxml
from xml.dom.minidom import parseString
import file_checker.util as util


class FileChecker():
    def __init__(self, settings={}):
        self.init_settings()
        self.load_settings(settings)

        self._error_info = []

    def init_settings(self):
        self._FILE_FORMATS = {}
        self._DIR_FORMATS = {}
        self._ONLY_FILES = []
        self._ONLY_DIRS = []
        self._IGNORE_FILES = []
        self._IGNORE_DIRS = []
        self._FILE_SEP = ''
        self._FILE_LETTER_CASE = ''
        self._DIR_SEP = ''
        self._DIR_LETTER_CASE = ''

    def convert_os_sep_of_str_in_list(self, strlist):
        # needs to test
        converted_strlist = []
        for s in strlist:
            converted_strlist.append(s.replace('/', os.sep))
        return converted_strlist

    def load_settings(self, settings={}):
        if 'FILE_FORMATS' in settings:
            self._FILE_FORMATS = settings['FILE_FORMATS']
            if 'SEP' in self._FILE_FORMATS:
                self._FILE_SEP = self._FILE_FORMATS['SEP']
            if 'LETTER_CASE' in self._FILE_FORMATS:
                self._FILE_LETTER_CASE = self._FILE_FORMATS['LETTER_CASE']
        if 'DIR_FORMATS' in settings:
            self._DIR_FORMATS = settings['DIR_FORMATS']
            if 'SEP' in self._DIR_FORMATS:
                self._DIR_SEP = self._DIR_FORMATS['SEP']
            if 'LETTER_CASE' in self._DIR_FORMATS:
                self._DIR_LETTER_CASE = self._DIR_FORMATS['LETTER_CASE']
        if 'ONLY_FILES' in settings:
            self._ONLY_FILES = settings['ONLY_FILES']
        if 'ONLY_DIRS' in settings:
            self._ONLY_DIRS = settings['ONLY_DIRS']
        if 'IGNORE_FILES' in settings:
            self._IGNORE_FILES = settings['IGNORE_FILES']
        if 'IGNORE_DIRS' in settings:
            self._IGNORE_DIRS = settings['IGNORE_DIRS']

        self._ONLY_FILES = self.convert_os_sep_of_str_in_list(
            self._ONLY_FILES)
        self._ONLY_DIRS = self.convert_os_sep_of_str_in_list(
            self._ONLY_DIRS)
        self._IGNORE_FILES = self.convert_os_sep_of_str_in_list(
            self._IGNORE_FILES)
        self._IGNORE_DIRS = self.convert_os_sep_of_str_in_list(
            self._IGNORE_DIRS)

    @property
    def error_info(self):
        return self._error_info

    @property
    def file_formats(self):
        return self._FILE_FORMATS

    @property
    def dir_formats(self):
        return self._DIR_FORMATS

    @property
    def only_files(self):
        return self._ONLY_FILES

    @property
    def only_dirs(self):
        return self._ONLY_DIRS

    @property
    def ignore_files(self):
        return self._IGNORE_FILES

    @property
    def ignore_dirs(self):
        return self._IGNORE_DIRS

    @property
    def file_sep(self):
        return self._FILE_SEP

    @property
    def file_letter_case(self):
        return self._FILE_LETTER_CASE

    @property
    def dir_sep(self):
        return self._DIR_SEP

    @property
    def dir_letter_case(self):
        return self._DIR_LETTER_CASE

    def is_string_matching(self, string, re_match_list=[]):
        if string:
            for pattern in re_match_list:
                if re.search(pattern, string) is not None:
                    return True
        return False

    def convert_walk_to_list(self, root):
        return [tp for tp in os.walk(os.path.realpath(root))]

    def get_root_in_walk(self, walk):
        root = ''
        if walk:
            root = walk[0][0]
            for (dirpath, dirs, files) in walk:
                if len(dirpath.split('/')) < len(root.split('/')):
                    root = dirpath
        return root

    def include_file_by_match_list_in_walk(self, re_patterns, walk, root=None):
        if root is None:
            root = self.get_root_in_walk(walk)

        filtered_walk = []
        for (dirpath, dirs, files) in walk:
            for pattern in re_patterns:
                filtered_files = []
                filename_pattern = pattern
                latest_sep_index = pattern.rfind(os.sep)

                # if pattern only apply to particular dir
                if latest_sep_index != -1:
                    dirname_pattern = pattern[:latest_sep_index] + '$'
                    filename_pattern = '^' + pattern[latest_sep_index + 1:]
                    rel_dirpath = dirpath[len(root):]
                    if not self.is_string_matching(
                       rel_dirpath, [dirname_pattern]):
                        continue

                for filename in files:
                    if self.is_string_matching(filename, [filename_pattern]):
                        filtered_files.append(filename)
                if filtered_files:
                    filtered_walk.append((dirpath, dirs, filtered_files))

        return filtered_walk

    def exclude_file_by_match_list_in_walk(self, re_patterns, walk, root=None):
        include_walk = self.include_file_by_match_list_in_walk(
            re_patterns, walk, root)
        filtered_walk = []

        for (dirpath, dirs, files) in walk:
            include_dirpath = ()

            for (dp, dn, fn) in include_walk:
                if dp == dirpath:
                    include_dirpath = (dp, dn, fn)

            if include_dirpath:
                filtered_files = []
                for filename in files:
                    if filename not in include_dirpath[2]:
                        filtered_files.append(filename)
                if filtered_files:
                    filtered_walk.append((dirpath, dirs, filtered_files))
            else:
                filtered_walk.append((dirpath, dirs, files))

        return filtered_walk

    def include_dir_by_match_list_in_walk(self, re_patterns, walk, root=None):
        if root is None:
            root = self.get_root_in_walk(walk)

        filtered_walk = []
        for (dirpath, dirs, files) in walk:
            rel_dirpath = dirpath[len(root):]
            if self.is_string_matching(rel_dirpath, re_patterns):
                filtered_walk.append((dirpath, dirs, files))

        return filtered_walk

    def exclude_dir_by_match_list_in_walk(self, re_patterns, walk, root=None):
        include_walk = self.include_dir_by_match_list_in_walk(
            re_patterns, walk, root)
        filtered_walk = []

        for (dirpath, dirs, files) in walk:
            include_dirpath = ()

            for (dp, dn, fn) in include_walk:
                if dp == dirpath:
                    include_dirpath = (dp, dn, fn)

            if not include_dirpath:
                filtered_walk.append((dirpath, dirs, files))

        return filtered_walk

    def get_file_list(self, walk):
        if self.only_files:
            walk = self.include_file_by_match_list_in_walk(
                self.only_files, walk)
        if self.ignore_files:
            walk = self.exclude_file_by_match_list_in_walk(
                self.ignore_files, walk)

        return walk

    def get_dir_list(self, walk):
        if self.only_dirs:
            walk = self.include_dir_by_match_list_in_walk(self.only_dirs, walk)
        if self.ignore_dirs:
            walk = self.exclude_dir_by_match_list_in_walk(
                self.ignore_dirs, walk)

        return walk

    def check_file(self, walk):
        walk = self.get_file_list(walk)
        for dirpath, dirs, files in walk:
            for f in files:
                extension = '.' + f.split(r'.')[-1]
                actual = f
                expect = actual.replace(extension, '')

                expect = util.convert_sep(expect, self.file_sep)
                expect = util.convert_sentence_to_case(
                    expect, self.file_letter_case)
                expect += extension

                if expect != actual:
                    self._error_info.append({
                        'filename': {
                            'expect': expect,
                            'actual': actual
                        },
                        'dirpath': dirpath
                    })

    def check_dir(self, walk):
        """
        Only check dirs/files path under root (excluded)
            root:     /root/path/to/dir
            dirpath:  /root/path/to/dir/SUBDIR
            settings: dir_format['letter_case'] = 'upper_case'

            OK: any part path of /root/path/to/dir will be never checked
        """
        walk = self.get_dir_list(walk)
        for dirpath, dirs, files in walk:
            actual = dirpath[dirpath.rfind(os.sep):]
            expect = actual
            expect = util.convert_sep(expect, self.dir_sep)
            expect = util.convert_sentence_to_case(
                expect, self.dir_letter_case)

            if expect != actual:
                self._error_info.append({
                    'dirname': {
                        'expect': expect,
                        'actual': actual
                    },
                    'dirpath': dirpath[:dirpath.rfind(os.sep)]
                })

    def check(self, root):
        root = os.path.realpath(root)
        walk = self.convert_walk_to_list(root)
        self.check_dir(walk)
        self.check_file(walk)

    def get_dict(self, error_info=None):
        return self.error_info

    def get_json(self, error_info=None):
        return json.dumps(self.error_info)

    def get_xml(self, error_info=None):
        return parseString(dicttoxml.dicttoxml(self.error_info)).toprettyxml()
