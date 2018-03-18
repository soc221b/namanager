import os
import json
from namanager.enums import FORMATS
from namanager.core import Namanager

SETTINGS_JSON = {}


def raiser(condition, msg):
    if not condition:
        raise Exception(msg)  # pragma: no cover


def import_settings(settings_file):
    global SETTINGS_JSON

    with open(settings_file, 'r') as s:
        SETTINGS_JSON = json.loads(s.read())

    raiser(isinstance(SETTINGS_JSON, dict),
           'settings must be dict.')

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
               '{0} must be {1}.'.format(key, value))

    for k, v in SETTINGS_JSON['FILE_FORMATS'].items():
        raiser(k in FORMATS,
               'FILE_FORMATS has wrong key:{0}.'.format(k))
        raiser(v in FORMATS[k],
               'FILE_FORMATS[\'{0}\'] has wrong key:{1}.'.format(k, v))

    for k, v in SETTINGS_JSON['DIR_FORMATS'].items():
        raiser(k in FORMATS,
               'DIR_FORMATS has wrong key:{0}.'.format(k))
        raiser(v in FORMATS[k],
               'DIR_FORMATS[\'{0}\'] has wrong key:{1}.'.format(k, v))


def main():  # pragma: no cover
    for d in SETTINGS_JSON['CHECK_DIRS']:
        checker = Namanager(SETTINGS_JSON)
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
        'namanager/namanager/settings.json')  # pragma: no cover
    main()  # pragma: no cover
