import file_checker.main as main # noqa


class TestMain():
    def test_import_settings(self):
        main.import_settings(settings_file='file_checker/settings.json')

    def test_main(self):
        main.import_settings(settings_file='file_checker/settings.json')
        main.main()
