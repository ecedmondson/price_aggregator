#!/bin/bash
export PYTHONPATH=$PWD

echo "Input venv name (default is venv):"
read venvname
echo "Starting virtual env."

#readonly sourcefile="./$venvname/bin/activate"
#source ${sourcefile}

source "$venvname/bin/activate"
pip3 install -r requirements.txt

source venv/bin/activate

python3 app.py
