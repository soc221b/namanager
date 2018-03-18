CWD=$(pwd)
NAMANAGER_ROOT_PATH="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/.."
cd $NAMANAGER_ROOT_PATH
error_code=0


assert()
{
    error=$?
    if [ $error -ne 0 ]; then
        echo "exit ($error)"
        error_code=1
    fi
}

deactivate

echo '''
================================================================================
Setting up a development environment
================================================================================
'''
python3 -m venv dev
assert
source ./dev/bin/activate
assert
echo "*** VIRTUAL_ENV: $VIRTUAL_ENV ***"
echo ""
pip install -r requirements_dev.txt
assert

echo '''
================================================================================
Unit tests
================================================================================
'''
mv tests namanager
assert
nosetests . -v --with-coverage --cover-erase --cover-html --cover-tests
assert
mv namanager/tests .
assert

echo '''
================================================================================
Flake8
================================================================================
'''
flake8 . bin/namanager --exclude dev,dist,build
assert

echo '''
================================================================================
Deactivate the development environment
================================================================================
'''
deactivate
assert

echo '''
================================================================================
Setting up a distribute environment
================================================================================
'''
python3 -m venv dist
assert
source ./dist/bin/activate
assert
echo "*** VIRTUAL_ENV: $VIRTUAL_ENV ***"
echo ""
python3 setup.py install
assert

echo '''
================================================================================
Run CLI
================================================================================
'''
namanager --settings namanager/settings.json
assert

echo '''
================================================================================
Deactivate the distribute environment
================================================================================
'''
deactivate
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
    source ./dev/bin/activate
    echo "*** VIRTUAL_ENV: $VIRTUAL_ENV ***"
    echo ""
    pip install -r requirements_dev.txt
fi

echo '''
================================================================================
'''
cd $CWD

if [ $error_code -eq 0 ]; then
    echo 'Passed'
else
    echo 'Error'
    exit 1
fi
