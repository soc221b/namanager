from file_checker.main import entry


class TestMain():
    def test_import_settings(self):
        pass

    def test_check(self):
        pass

    def test_entry(self):
        entry('file_checker/settings.json', False)
