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
    def __init__(self):
        self.result = {'errors': []}

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
        for path in os.listdir(os.getcwd()):
            if path.startswith('namanager_rename_'):
                backup_files.append(path)
        return backup_files

    def revert(self, **kwargs):
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
                    self.result['errors'].append(
                        'There are so many backup files, please specify file.')
            elif len(backup_files) == 0:
                self.result['errors'].append(
                    'No backup file are detected, please specify file.')

        try:
            am = ArchieveManager()
            with open(REVERT_FILE, 'r') as f:
                am.rename(json.loads(f.read()))
        except Exception as e:
            self.result['errors'].append(e)

    def check(self, **kwargs):
        settings_json = kwargs.get(
            'settings_json',
            self.import_settings(os.path.join(os.getcwd(), 'settings.json')))
        COUNT = kwargs.get('count', False)
        FMT = kwargs.get('fmt', 'json')
        PRETTY_DUMP = kwargs.get('pretty_dump', False)
        unexpected_pairs = []
        checker = Namanager(settings_json)

        for d in settings_json['CHECK_DIRS']:
            checker.check(d)

            if checker.error_info:
                unexpected_pairs.extend(checker.error_info)
                if COUNT:
                    self.result['errors'].append(
                        'In folder {0} :'.format(os.path.realpath(d)))
                    self.result['errors'].append(
                        'FAILED (error={0})'.format(checker.error_info_count))

        if FMT == 'readable':
            s = ""
            for pair in checker.get_dict(unexpected_pairs):
                s += 'expect: {0}\n'.format(pair['expect'])
                s += 'actual: {0}\n\n'.format(pair['actual'])
            self.result['unexpected_pairs'] = s
        elif FMT == 'json':
            self.result['unexpected_pairs'] = (
                checker.get_json(unexpected_pairs, PRETTY_DUMP))
        elif FMT == 'xml':
            self.result['unexpected_pairs'] = (
                checker.get_xml(unexpected_pairs, PRETTY_DUMP))
        elif FMT == 'nodump':
            self.result['unexpected_pairs'] = (
                checker.get_dict(unexpected_pairs))

    def rename_backup(self, rename_pairs, **kwargs):
        am = ArchieveManager()
        RENAME_BACKUP = kwargs.get('rename_backup', False)
        RENAME_BACKUP_DIR = kwargs.get('rename_backup_dir', os.getcwd())

        if RENAME_BACKUP:
            test_writing_permission(dirname=RENAME_BACKUP_DIR)
            revert_pairs = am.gen_revert_path_pairs(rename_pairs)
            self.result['rename_backup_name'] = os.sep.join([
                RENAME_BACKUP_DIR,
                self.get_bak_filename(prefix='namanager_rename_')])
            with open(self.result['rename_backup_name'], 'w') as f:
                f.write(json.dumps(revert_pairs, indent=4, sort_keys=True))

    def rename(self, rename_pairs, **kwargs):
        RENAME_RECOVER = kwargs.get('rename_recover', False)
        am = ArchieveManager()
        rename_pairs = self.get_src_dst_pair(rename_pairs)
        self.rename_backup(rename_pairs, **kwargs)

        error_pairs = am.rename(rename_pairs)

        if error_pairs:
            # TODO: output more information
            if RENAME_RECOVER:
                # try to directly revert all paths
                recover_pairs = am.gen_revert_path_pairs(rename_pairs)
                am.rename(recover_pairs)
                self.result['errors'].append("Failed to rename (Recovered).")

            else:
                self.result['errors'].append('Some paths can not be renamed.')

    def entry(self, **kwargs):
        REQUIRED = kwargs.get('required', False)
        VERSION = kwargs.get('version', False)
        REVERT = kwargs.get('revert', False)
        RENAME = kwargs.get('rename', False)

        if VERSION:
            import namanager
            print(namanager.__version__)

        elif RENAME:
            SETTINGS = kwargs.get('settings', False)
            if SETTINGS:
                kwargs['settings_json'] = self.import_settings(SETTINGS)
            kwargs['fmt'] = 'nodump'
            self.check(**kwargs)
            self.rename(self.result['unexpected_pairs'], **kwargs)

        elif REVERT:
            self.revert(**kwargs)

        else:
            SETTINGS = kwargs.get('settings', False)
            if SETTINGS:
                kwargs['settings_json'] = self.import_settings(SETTINGS)
            self.check(**kwargs)
            print(self.result['unexpected_pairs'])

        if self.result['errors']:
            for e in self.result['errors']:
                print(e)
            if REQUIRED:
                exit(1)
