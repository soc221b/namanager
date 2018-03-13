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
                                      Nose
================================================================================
'''
nosetests . -v --with-coverage --cover-erase --cover-html
assert

echo '''
================================================================================
                                     Flake8
================================================================================
'''
flake8 . --exclude env
assert

echo '''
================================================================================
                                   Run tests
================================================================================
'''
python3 tests/test_util.py
assert

python3 tests/test_file_checker.py
assert

echo '''
================================================================================
                                   Run main
================================================================================
'''
python3 src/file_checker.py
assert

echo '''
================================================================================
'''
if [ $error_code -eq 0 ]; then
    echo 'Passed'
else
    echo 'Error'
    exit 1
fi

cd $cwd
