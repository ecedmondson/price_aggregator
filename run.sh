#!/bin/bash
export PYTHONPATH=$PWD

echo "Input venv name (default is venv):"
read venvname
echo "Starting virtual env."

#readonly sourcefile="./$venvname/bin/activate"
#source ${sourcefile}

source "$venvname/bin/activate"
pip3 install -r requirements.txt

export FLASK_APP=app.py
export FLASK_DEBUG=1
python3 -m flask run -h 0.0.0.0 -p 9578 --reload
