import os
import re
from enums import FORMATS
from settings import (CHECK_DIRS, FILE_FORMATS, DIR_FORMATS,
                      IGNORE_FILES, IGNORE_DIRS)


class FileChecker():
    def __init__(self):
        self.error_list = []

    def is_file_ignored(self, filename):
        for pattern in IGNORE_FILES:
            if re.match(pattern, filename):
                return True
        return False

    def is_dir_ignored(self, dirname):
        for pattern in IGNORE_DIRS:
            if re.match(pattern, dirname):
                return True
        return False

    def convert_sep(self, name, formats_):
        for f in formats_:
            if f == 'dash_to_underscore':
                name = name.replace('-', '_')
            if f == 'underscore_to_dash':
                name = name.replace('_', '-')
        return name

    def convert_alphabet(self, name, formats_):
        try:
            for f in formats_:
                if f == 'upper_case':
                    name = name.upper()
                if f == 'lower_case':
                    name = name.lower()
                if f == 'camel_case':
                    pass
                if f == 'pascal_case':
                    pass
        except Exception:
            pass

        return name

    def _convert_filename(self, filename):
        pass

    def _convert_dirname(self, dirname):
        pass

    def check(self, root):
        for (dirpath, dirname, filename) in os.walk(root):
            pass


def check_settings():
    if not isinstance(CHECK_DIRS, list):
        raise Exception('CHECK_DIRS must be list.')
    if not isinstance(IGNORE_FILES, list):
        raise Exception('IGNORE_FILES must be list.')
    if not isinstance(IGNORE_DIRS, list):
        raise Exception('IGNORE_DIRS must be list.')
    if not isinstance(FILE_FORMATS, dict):
        raise Exception('FILE_FORMATS must be dict.')
    if not isinstance(DIR_FORMATS, dict):
        raise Exception('DIR_FORMATS must be dict.')

    for k, v in FILE_FORMATS.items():
        if k not in FORMATS:
            raise Exception('FILE_FORMATS has wrong key.')
        elif v not in FORMATS[k]:
            raise Exception('FILE_FORMATS[\'{0}\'] has wrong key.'.format(k))

    for k, v in DIR_FORMATS.items():
        if k not in FORMATS:
            raise Exception('DIR_FORMATS has wrong key.')
        elif v not in FORMATS[k]:
            raise Exception('DIR_FORMATS[\'{0}\'] has wrong key.'.format(k))


if __name__ == '__main__':
    check_settings()

    checker = FileChecker()
    for d in CHECK_DIRS:
        checker.check(d)

    for e in checker.error_list:
        print(e)
