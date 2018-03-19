################################################################################
# Set up
################################################################################

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

# '2 7 14' or '3 6 4', etc.
VERSION=`$PYTHON -c 'import sys; print("%i %i %i" % (sys.version_info[0], sys.version_info[1], sys.version_info[2]))'`
VERSION=($VERSION)
VERSION_MAJOR=${VERSION[0]}
VERSION_MINOR=${VERSION[1]}
VERSION_PATCH=${VERSION[2]}
################################################################################
# Functions
################################################################################

assert()
{
    error=$?
    if [ $error -ne 0 ]; then
        echo "exit ($error)"
        error_code=1
    fi
}

is_supports_venv()
{
    if [[ VERSION_MAJOR -ge 3 ]] && [[ VERSION_MINOR -ge 3 ]]; then
        is_supports=1
    else
        is_supports=0
    fi

    return $is_supports
}

# pass name to $1
activate_env()
{
    is_supports_venv
    if [[ $? -eq 1 ]]; then
        $PYTHON -m venv $1
        assert
        source ./$1/bin/activate
        assert
        echo "*** VIRTUAL_ENV: $VIRTUAL_ENV ***"
        echo ""
    fi
}

# pass name to $1
deactivate_env()
{
    is_supports_venv
    if [[ $? -eq 1 ]]; then
        deactivate
        assert
    fi
}

################################################################################
# Main
################################################################################
echo $SHELL
echo `which $PIP`
echo `which $PYTHON`
echo ""

echo '''
================================================================================
Tearing down environment
================================================================================
'''
deactivate
rm -rf dev dist
$PIP uninstall -y -r requirements_dev.txt
$PIP uninstall -y -r requirements.txt

echo '''
================================================================================
Setting up a development environment
================================================================================
'''
activate_env dev
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
deactivate_env dev

echo '''
================================================================================
Setting up a distribute environment
================================================================================
'''
activate_env dist
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
deactivate_env dist

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
