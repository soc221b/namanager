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

if [ "`$PIP -V`" != "`$PYTHON -m pip -V`" ]; then
    $PIP -V
    $PYTHON -V
    echo "Version of pip and python must be same."
    echo
    echo "Add version suffix as argument if you wnat to specify version."
    echo "example: your python command is 'python3.6' => type './test.sh 3.6'"
    exit 1
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
# you could pass expect error-code to $1
assert()
{
    error=$?
    if [[ $# -eq 1 ]]; then
        if [ $error -ne $1 ]; then
            echo "exit ($error)"
            error_code=1
        fi
    else
        if [ $error -ne 0 ]; then
            echo "exit ($error)"
            error_code=1
        fi
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
        $PYTHON -m venv env/$1
        assert
        source ./env/$1/bin/activate
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
    fi
}

# -d: make dir
mktemp_cwd()
{
    existed='blah'
    while [[ $existed != '' ]]; do
        rand=`openssl rand -base64 16`
        rand=${rand//\//_}
        existed=`ls | grep $rand`
    done

    temp_type=false
    for p in $@; do
        if [[ $p = '-d' ]]; then temp_type=true; fi
    done

    if [[ $temp_type = true ]]; then mkdir $rand; else touch $rand; fi

    result=$rand
}

################################################################################
# Main
################################################################################
echo '''
================================================================================
Environment information
================================================================================
'''
echo $SHELL
echo `which $PIP`
echo `which $PYTHON`
echo `$PIP -V`
echo `$PYTHON -V`

echo '''
================================================================================
Tearing down environment
================================================================================
'''
deactivate
rm -rf env build dist
mv namanager/tests .

# Prevent haven't completely install the package.

# Try to correctly install namanager and remove it.
$PIP install namanager
$PIP uninstall -y namanager

# Initialize libs.
$PIP uninstall -y -r requirements_dev.txt
$PIP uninstall -y -r requirements.txt

# Check if the namanager has been installed or hasn't completely installed.
version=`namanager --version 2>/dev/null`
assert 127 # command not found

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
Flake8
================================================================================
'''
flake8 . bin/namanager --exclude env
assert

echo '''
================================================================================
Rebuild local development environment
================================================================================
'''
activate_env dev
$PIP install -r requirements_dev.txt

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
