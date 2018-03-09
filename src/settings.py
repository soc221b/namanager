import os


CHECK_DIRS = [os.sep.join([os.path.dirname(__file__), 'code'])]

IGNORE_FILES = [r".*\.md$"]

IGNORE_DIRS = [os.sep.join([r'.*', r'unclassified$']),
               os.sep.join([r'.*', r'unclassified', r'.*$'])]

FILE_FORMATS = {'letter_case': 'lower_case',
                'sep': 'dash_to_underscore',
                'abbr': 'convert'}

DIR_FORMATS = {}
