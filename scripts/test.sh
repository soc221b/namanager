cwd=$(pwd)
file_checker_root_path="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/.."
cd $file_checker_root_path
error_code=0


assert()
{
    error=$?
    if [ $error -ne 0 ]; then
        echo "exit ($error)"
        error_code=1
    fi
}

echo '''
================================================================================
                        Setting up a development environment
================================================================================
'''
pip install -r requirements_dev.txt
assert

echo '''
================================================================================
                                      Nose
================================================================================
'''
mv tests file_checker
assert
nosetests . -v --with-coverage --cover-erase --cover-html --cover-tests
assert
mv file_checker/tests .
assert

echo '''
================================================================================
                                     Flake8
================================================================================
'''
flake8 . bin/file_checker --exclude env,build
assert

echo '''
================================================================================
                         Setting up a client environment
================================================================================
'''
pip uninstall -r requirements_dev.txt -y
assert
pip install -r requirements.txt
assert

echo '''
================================================================================
                                   Setup module
================================================================================
'''
python3 setup.py install
assert

echo '''
================================================================================
                                     Run main
================================================================================
'''
cp file_checker/main.py ../
cd ../
python3 FileChecker/file_checker/main.py
assert
cd FileChecker
assert


echo '''
================================================================================
                                     Run CLI
================================================================================
'''
file_checker --settings file_checker/settings.json
assert

if [ $CI ]; then
    if [ $error_code -eq 0 ]; then
        echo '''
================================================================================
                               Update codecov badge
================================================================================
'''
        pip install coverage codecov
        codecov --required
        assert
    fi
else
    echo '''
================================================================================
                      Rebuild local development environment
================================================================================
'''
    pip install -r requirements_dev.txt
fi

echo '''
================================================================================
'''
cd $cwd

if [ $error_code -eq 0 ]; then
    echo 'Passed'
else
    echo 'Error'
    exit 1
fi
