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

    SETTING_TYPE_PAIR = {
        'CHECK_DIRS': list,
        'ONLY_FILES': list,
        'ONLY_DIRS': list,
        'IGNORE_FILES': list,
        'IGNORE_DIRS': list,
        'FILE_FORMATS': dict,
        'DIR_FORMATS': dict
    }

    for key, value in SETTING_TYPE_PAIR.items():
        SETTINGS_JSON[key] = SETTINGS_JSON.get(key, value())
        raiser(isinstance(SETTINGS_JSON[key], value),
               Exception('{0} must be {1}.'.format(key, value)))

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


def main():  # pragma: no cover
    for d in SETTINGS_JSON['CHECK_DIRS']:
        checker = FileChecker(SETTINGS_JSON)
        checker.check(d)

        RESULT = checker.get_dict()
        for e in RESULT:
            print(e)

        print('In folder {0} :'.format(os.path.realpath(d)))
        if RESULT:
            print('FAILED (error{0}={1})\n'.format(
                  's' if len(RESULT) > 1 else '',
                  len(RESULT)))
        else:
            print('OK.\n')


if __name__ == '__main__':
    import_settings(
        'FileChecker/file_checker/settings.json')  # pragma: no cover
    main()  # pragma: no cover
