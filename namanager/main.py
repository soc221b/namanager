import os
import json
import datetime
import sys
from namanager.core import Namanager
from namanager.archieve_manager import ArchieveManager


def raiser(condition, msg):
    if not condition:
        raise Exception(msg)  # pragma: no cover


def test_writing_permission(**kwargs):
    """
    param dirname:
    type dirname: str
    param required: default True
    type required: True, False
    param error_msg:
    type error_msg: str
    """

    try:
        dirname = kwargs.get('dirname', os.getcwd())
        if dirname[-1] != os.sep:
            dirname += os.sep
        # test directory is exists or not and raise
        os.path.realpath(dirname)

        filename = ''.join([dirname, 'test_file'])
        while os.path.exists(filename):
            filename += '_'

        with open(filename, 'w') as f:
            f.write('test...')
        os.remove(filename)

    except Exception as e:
        print(kwargs.get('error_msg', ''))
        required = kwargs.get('required', True)
        if required:
            raise e


class Driver():
    def import_settings(self, settings_file):
        settings_json = {}
        try:
            with open(settings_file, 'r') as s:
                settings_json = json.loads(s.read())
        except Exception as e:
            file_not_found = False
            if sys.version_info[0] >= 3:
                if isinstance(e, FileNotFoundError):  # noqa: F821
                    file_not_found = True
            elif isinstance(e, IOError):  # noqa: F821
                file_not_found = True
            if file_not_found:
                print('File: {0} not found'.format(settings_file))
            else:
                raise e

        raiser(isinstance(settings_json, dict), 'settings must be dict.')

        return settings_json

    def get_src_dst_pair(self, error_info):
        # we need to move this function to/into a better place
        src_dst_pair = []

        for e in error_info:
            src_dst_pair.append([e['actual'], e['expect']])

        return src_dst_pair

    def get_bak_filename(self, **kwargs):
        prefix = kwargs.get('prefix', '')
        when = kwargs.get('when', '{:%Y%m%d%H%M%S}'.format(
            datetime.datetime.now()))

        return prefix + when + '.bak'

    def find_recent_backup_files(self):
        backup_files = []
        for path in os.listdir():
            if path.startswith('namanager_rename_'):
                backup_files.append(path)
        return backup_files

    def revert(self, **kwargs):
        result = {'errors': []}
        REVERT_FILE = kwargs.get('revert_file', None)
        REVERT_LAST = kwargs.get('revert_last', False)
        if REVERT_FILE is None or REVERT_LAST:
            backup_files = self.find_recent_backup_files()
            if len(backup_files) == 1:
                REVERT_FILE = backup_files[0]
            elif len(backup_files) > 1:
                if REVERT_LAST:
                    backup_files.sort(reverse=True)
                    REVERT_FILE = backup_files[0]
                else:
                    result['errors'].append(
                        'There are so many backup files, please specify file.')
            elif len(backup_files) == 0:
                result['errors'].append(
                    'No backup file are detected, please specify file.')

        try:
            am = ArchieveManager()
            with open(REVERT_FILE, 'r') as f:
                am.rename(json.loads(f.read()))
        except Exception as e:
            result['errors'].append(e)
        return result

    def check(self, **kwargs):
        result = {'errors': [], 'unexpected_pairs': []}
        settings_json = kwargs.get(
            'settings_json',
            self.import_settings(os.path.join(os.getcwd(), 'settings.json')))
        FMT = kwargs.get('fmt', 'json')
        PRETTY_DUMP = kwargs.get('pretty_dump', False)
        error_infos = []

        for d in settings_json['CHECK_DIRS']:
            checker = Namanager(settings_json)
            checker.check(d)

            if checker.error_info:
                error_infos.extend(checker.error_info)

                result['errors'].append(
                    'In folder {0} :'.format(os.path.realpath(d)))
                result['errors'].append(
                    'FAILED (error={0})'.format(checker.error_info_count))

        if FMT == 'dict':
            print(checker.get_dict(error_infos))
        elif FMT == 'json':
            print(checker.get_json(error_infos, PRETTY_DUMP))
        elif FMT == 'xml':
            print(checker.get_xml(error_infos, PRETTY_DUMP))
        elif FMT == 'nodump':
            result['unexpected_pairs'].extend(checker.get_dict(error_infos))

        return result

    def rename(self, rename_pairs, **kwargs):
        result = {'errors': []}
        RENAME_BACKUP = kwargs.get('rename_backup', False)
        RENAME_BACKUP_DIR = kwargs.get('rename_backup_dir', os.getcwd())
        RENAME_RECOVER = kwargs.get('rename_recover', False)

        if RENAME_BACKUP:
            test_writing_permission(dirname=RENAME_BACKUP_DIR)

        am = ArchieveManager()
        rename_pairs = self.get_src_dst_pair(rename_pairs)

        if RENAME_BACKUP:
            revert_pairs = am.gen_revert_path_pairs(rename_pairs)
            filename = self.get_bak_filename(prefix='namanager_rename_')
            with open(os.sep.join([RENAME_BACKUP_DIR, filename]),
                      'w') as f:
                f.write(json.dumps(revert_pairs, indent=4, sort_keys=True))

        error_pairs = am.rename(rename_pairs)

        if error_pairs:
            # TODO: output more information
            if RENAME_RECOVER:
                # try to directly revert all paths
                recover_pairs = am.gen_revert_path_pairs(rename_pairs)
                am.rename(recover_pairs)
                result['errors'].append("Failed to rename (Recovered).")

            else:
                result['errors'].append('Some paths can not be renamed.')

        return result

    def entry(self, **kwargs):
        REQUIRED = kwargs.get('required', False)
        VERSION = kwargs.get('version', False)
        REVERT = kwargs.get('revert', False)
        RENAME = kwargs.get('rename', False)
        errors = []

        if VERSION:
            import namanager
            print(namanager.__version__)

        elif RENAME:
            SETTINGS = kwargs.get('settings', False)
            if SETTINGS:
                kwargs['settings_json'] = self.import_settings(SETTINGS)
            kwargs['fmt'] = 'nodump'
            result = self.check(**kwargs)
            errors.extend(result['errors'])
            unexpected_pairs = result['unexpected_pairs']

            result = self.rename(unexpected_pairs, **kwargs)
            errors.extend(result['errors'])

        elif REVERT:
            result = self.revert(**kwargs)
            errors.extend(result['errors'])

        else:
            SETTINGS = kwargs.get('settings', False)
            if SETTINGS:
                kwargs['settings_json'] = self.import_settings(SETTINGS)
            result = self.check(**kwargs)
            errors.extend(result['errors'])

        if errors:
            for e in errors:
                print(e)
            if REQUIRED:
                exit(1)
