from file_checker.main import import_settings, main


class TestMain():
    def test_import_settings(self):
        import_settings(settings_file='file_checker/settings.json')

    def test_main(self):
        import_settings(settings_file='file_checker/settings.json')
        main()
