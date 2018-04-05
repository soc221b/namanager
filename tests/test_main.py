import os
import time
import namanager.tests.helper as helper
from namanager.main import Driver
# from filelock import FileLock


class TestMain():
    def __init__(self):
        self.TMPFILE_PREFIX = 'test_main_'
        self.RENAME_SUFFIX = '_*&^%$'
        self.TMP_ROOT = os.sep.join(
            [os.path.realpath(os.path.dirname(__file__)), 'test_root'])
        if not os.path.exists(self.TMP_ROOT):
            os.mkdir(self.TMP_ROOT)

    def test_import_settings(self):
        pass

    def test_check(self):
        pass

    def test_cli_version(self):
        driver = Driver()
        kwargs = {
            'version': True,
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_settings(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_required(self):
        pass

    def test_cli_with_readable(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'readable',
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_with_xml(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'xml',
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_with_json(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'json',
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_xml_pretty_dump(self):
        driver = Driver()
        kwargs_xml = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'xml',
            'pretty_dump': True,
        }

        driver.entry(**kwargs_xml)

        assert driver.result['errors'] == []

    def test_cli_json_pretty_dump(self):
        driver = Driver()
        kwargs_json = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'json',
            'pretty_dump': True,
        }

        driver.entry(**kwargs_json)

        assert driver.result['errors'] == []

    def test_cli_rename(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                    "SEP": ["dash_to_underscore"],
                },
            },
            'rename': True,
        }

        driver.entry(**kwargs)

        os.remove(driver.result['rename_backup_name'])
        assert driver.result['errors'] == []

    def test_cli_rename_backup(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup': True,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**kwargs)

        os.remove(driver.result['rename_backup_name'])
        assert driver.result['errors'] == []

    def test_cli_rename_no_backup(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup': False,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**kwargs)

        assert driver.find_recent_backup_files() == []
        assert driver.result['errors'] == []

    def test_cli_rename_backup_dir(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup_dir': dirs[0],
        }
        assert driver.find_recent_backup_files(dirname=dirs[0]) == []

        driver.entry(**kwargs)

        assert driver.find_recent_backup_files(dirname=dirs[0]) != []
        os.remove(driver.result['rename_backup_name'])
        assert driver.result['errors'] == []

    def _test_cli_rename_recover(self):
        return

        """
        Can not to create error for test recover mode
        tried:
            1. lock file
        """

        # driver = Driver()
        # dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
        #                        prefix=self.TMPFILE_PREFIX)
        # files = helper.mktemps(3, root=dirs[0], prefix=self.TMPFILE_PREFIX)
        # kwargs = {
        #     'settings_json': {
        #         'CHECK_DIRS': dirs,
        #         "FILE_FORMATS": {"LETTER_CASE": "upper_case"}},
        #     'rename': True, 'rename_recover': True,
        # }
        # with FileLock(files[0]):
        #     driver.entry(**kwargs)

        # os.remove(driver.result['rename_backup_name'])
        # assert driver.result['errors'] != []

    def test_cli_revert(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        rename_kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {"LETTER_CASE": "upper_case"}},
            'rename': True, 'rename_backup': True,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []
        driver.entry(**rename_kwargs)
        assert driver.find_recent_backup_files() != []
        revert_kwargs = {
            'revert': True,
        }

        driver.entry(**revert_kwargs)

        os.remove(driver.result['rename_backup_name'])
        assert driver.result['errors'] == []

    def test_cli_revert_last_existed(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        rename_kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {"LETTER_CASE": "upper_case"}},
            'rename': True, 'rename_backup': True,
        }
        revert_kwargs = {'revert': True, 'revert_last': True}
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        # rename 1
        driver.entry(**rename_kwargs)
        assert len(driver.find_recent_backup_files()) == 1
        first_backup = driver.result['rename_backup_name']

        # rename 2
        rename_kwargs['settings_json']['DIR_FORMATS']['LETTER_CASE'] = (
            'lower_case')
        # prevent write to same filename
        time.sleep(1)
        driver.entry(**rename_kwargs)
        assert len(driver.find_recent_backup_files()) == 2
        second_backup = driver.result['rename_backup_name']

        # revert 2
        driver.entry(**revert_kwargs)
        os.remove(second_backup)
        assert len(driver.find_recent_backup_files()) == 1

        # revert 1
        driver.entry(**revert_kwargs)

        os.remove(first_backup)
        assert driver.result['errors'] == []

    def test_cli_revert_last_not_existed(self):
        driver = Driver()
        revert_kwargs = {'revert': True, 'revert_last': True}
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**revert_kwargs)

        assert driver.result['errors'] != []

    def test_cli_revert_file(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        rename_kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {"LETTER_CASE": "upper_case"}},
            'rename': True, 'rename_backup': True,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []
        driver.entry(**rename_kwargs)
        assert driver.find_recent_backup_files() != []
        revert_kwargs = {
            'revert': True, 'revert_file': driver.result['rename_backup_name']
        }

        driver.entry(**revert_kwargs)

        os.remove(driver.result['rename_backup_name'])
        assert driver.result['errors'] == []

    def test_required(self):
        driver = Driver()
        revert_kwargs = {'revert': True, 'revert_last': True, 'required': True}
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**revert_kwargs)

        assert driver.exit_code != 0
