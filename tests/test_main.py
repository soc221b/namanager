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

                entry('namanager/settings.json', **kwargs)
