CWD=$(pwd)
NAMANAGER_ROOT_PATH="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/.."
cd $NAMANAGER_ROOT_PATH
error_code=0

# changes version which user defined
# pass version to $1
if [ $# -eq 1 ]; then
    PIP=`which pip$1`
    PYTHON=`which python$1`
else
    PIP=`which pip`
    PYTHON=`which python`
fi

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
Tearing down environment
================================================================================
'''
if [ $CI ]; then
    deactivate
    rm -rf dev dist
fi

echo '''
================================================================================
Setting up a development environment
================================================================================
'''
$PYTHON -m venv dev
assert
source ./dev/bin/activate
assert
echo "*** VIRTUAL_ENV: $VIRTUAL_ENV ***"
echo ""
$PIP install -r requirements_dev.txt
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
$PYTHON -m venv dist
assert
source ./dist/bin/activate
assert
echo "*** VIRTUAL_ENV: $VIRTUAL_ENV ***"
echo ""
$PYTHON setup.py install
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
        $PIP install coverage codecov
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
    $PIP install -r requirements_dev.txt
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
