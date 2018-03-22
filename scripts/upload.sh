cwd=$(pwd)
namanager_root_path="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/.."
cd $namanager_root_path

python3 -m venv upload
source ./upload/bin/activate

pip install twine
pip install sdist
python setup.py sdist
pip install wheel
python setup.py bdist_wheel --universal
twine upload dist/*

cd $CWD