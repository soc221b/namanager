import os
import re


class FileChecker():
    def __init__(self, settings={}):
        self.init_settings()
        self.load_settings(settings)

        self._error_set = set()

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
    def error_set(self):
        return self._error_set

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
        for pattern in re_match_list:
            if re.match(pattern, string):
                return True
        return False

    def check(self, root):
        for (dirpath, dirname, filename) in os.walk(root):
            pass
