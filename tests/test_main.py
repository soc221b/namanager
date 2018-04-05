from namanager.main import entry


class TestMain():
    def test_import_settings(self):
        pass

    def test_check(self):
        pass

    def test_entry(self):
        # no test for `required`
        for fmt in ['xml', 'json', 'dict']:
            for pretty_dump in [True, False]:
                if fmt:
                    kwargs = {
                        'required': False,
                        'pretty_dump': pretty_dump,
                    }
                else:
                    kwargs = {
                        'required': False,
                        'fmt': fmt,
                        'pretty_dump': pretty_dump,
                    }
                kwargs['settings'] = 'namanager/settings.json'
                entry(**kwargs)

    def test_cli_version(self):
        kwargs = {
            'version': True,
        }
        entry(**kwargs)

    def test_cli_settings(self):
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
        }
        entry(**kwargs)

    def test_cli_required(self):
        pass

    def test_cli_with_readable(self):
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'dict',
        }
        entry(**kwargs)

    def test_cli_with_xml(self):
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'xml',
        }
        entry(**kwargs)

    def test_cli_with_json(self):
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'json',
        }
        entry(**kwargs)

    def test_cli_pretty_dump(self):
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'json',
            'pretty_dump': True,
        }
        entry(**kwargs)
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'xml',
            'pretty_dump': True,
        }
        entry(**kwargs)

    def test_cli_rename(self):
        pass

    def test_cli_rename_backup(self):
        pass

    def test_cli_rename_no_backup(self):
        pass

    def test_cli_rename_backup_dir(self):
        pass

    def test_cli_rename_recover(self):
        pass

    def test_cli_revert(self):
        pass

    def test_cli_revert_last(self):
        pass

    def test_cli_revert_file(self):
        pass
