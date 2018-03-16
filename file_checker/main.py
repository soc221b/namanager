import os
import json
from file_checker.enums import FORMATS
from file_checker.core import FileChecker

SETTINGS_JSON = {}


def raiser(condition, msg):
    if not condition:
        raise Exception('settings must be dict.')  # pragma: no cover


def import_settings(settings_file):
    global SETTINGS_JSON

    with open(settings_file, 'r') as s:
        SETTINGS_JSON = json.loads(s.read())

    raiser(isinstance(SETTINGS_JSON, dict),
           Exception('settings must be dict.'))

    SETTINGS_JSON['CHECK_DIRS'] = SETTINGS_JSON.get('CHECK_DIRS', [])
    raiser(isinstance(SETTINGS_JSON['CHECK_DIRS'], list),
           Exception('CHECK_DIRS must be list.'))

    SETTINGS_JSON['ONLY_FILES'] = SETTINGS_JSON.get('ONLY_FILES', [])
    raiser(isinstance(SETTINGS_JSON['ONLY_FILES'], list),
           Exception('ONLY_FILES must be list.'))

    SETTINGS_JSON['ONLY_DIRS'] = SETTINGS_JSON.get('ONLY_DIRS', [])
    raiser(isinstance(SETTINGS_JSON['ONLY_DIRS'], list),
           Exception('ONLY_DIRS must be list.'))

    SETTINGS_JSON['IGNORE_FILES'] = SETTINGS_JSON.get('IGNORE_FILES', [])
    raiser(isinstance(SETTINGS_JSON['IGNORE_FILES'], list),
           Exception('IGNORE_FILES must be list.'))

    SETTINGS_JSON['IGNORE_DIRS'] = SETTINGS_JSON.get('IGNORE_DIRS', [])
    raiser(isinstance(SETTINGS_JSON['IGNORE_DIRS'], list),
           Exception('IGNORE_DIRS must be list.'))

    SETTINGS_JSON['FILE_FORMATS'] = SETTINGS_JSON.get('FILE_FORMATS', {})
    raiser(isinstance(SETTINGS_JSON['FILE_FORMATS'], dict),
           Exception('FILE_FORMATS must be dict.'))

    SETTINGS_JSON['DIR_FORMATS'] = SETTINGS_JSON.get('DIR_FORMATS', {})
    raiser(isinstance(SETTINGS_JSON['DIR_FORMATS'], dict),
           Exception('DIR_FORMATS must be dict.'))

    for k, v in SETTINGS_JSON['FILE_FORMATS'].items():
        raiser(k in FORMATS,
               Exception('FILE_FORMATS has wrong key.'))
        raiser(v in FORMATS[k],
               Exception('FILE_FORMATS[\'{0}\'] has wrong key.'.format(k)))

    for k, v in SETTINGS_JSON['DIR_FORMATS'].items():
        raiser(k in FORMATS,
               Exception('DIR_FORMATS has wrong key.'))
        raiser(v in FORMATS[k],
               Exception('DIR_FORMATS[\'{0}\'] has wrong key.'.format(k)))


def check(required=False, fmt='json'):  # pragma: no cover
    for d in SETTINGS_JSON['CHECK_DIRS']:
        checker = FileChecker(SETTINGS_JSON)
        checker.check(d)

        if fmt == 'readable':
            RESULT = checker.get_dict()
            for e in RESULT:
                print(e)
        else:
            if fmt == 'dict':
                RESULT = checker.get_dict()
            elif fmt == 'json':
                RESULT = checker.get_json()
            elif fmt == 'xml':
                RESULT = checker.get_xml()
            print(RESULT)

        print('In folder {0} :'.format(os.path.realpath(d)))
        if RESULT:
            print('FAILED (error{0}={1})\n'.format(
                  's' if len(RESULT) > 1 else '',
                  len(RESULT)))
            if required:
                exit(1)
        else:
            print('OK.\n')


def entry(settings_file, required=False, fmt='json'):
    import_settings(settings_file)
    check(required, fmt)


if __name__ == '__main__':
    entry('FileChecker/file_checker/settings.json')
