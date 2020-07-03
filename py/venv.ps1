
# PowerShell script to delete or create the Python Virtual Environment.
# Requires Python 3; version 3.7 or higher recommended.
# Chris Joakim, Microsoft, 2020/07/03

echo 'upgrading pip ...'
python -m pip install --upgrade pip

echo 'creating new venv ...'
python -m venv .

echo 'activating new venv ...'
.\Scripts\Activate.ps1
python --version
pip --version

rm .\requirements.txt

echo 'pip-compile requirements.in ...'
pip-compile --output-file .\requirements.txt .\requirements.in

echo 'pip install requirements.txt ...'
pip install -r .\requirements.txt

echo 'pip list ...'
pip list

echo 'done'
