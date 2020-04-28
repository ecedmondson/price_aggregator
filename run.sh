#!/bin/bash
export PYTHONPATH=$PWD

echo "Input venv name (default is venv):"
read venvname
echo "Starting virtual env."

#readonly sourcefile="./$venvname/bin/activate"
#source ${sourcefile}

source "$venvname/bin/activate"
pip3 install -r requirements.txt

CHROME=$(python3 bin/chrome_compatibility.py)
if [[ $CHROME -eq 0 ]]
then
    echo "Google Chrome stable and chromedriver seem compatible. No install needed."
fi

if [[ -n $CHROME ]]
then
    echo "Chromedriver seemed incompatible. Attempting install."
    pip3 install chromedriver_installer \
        --install-option="--chromedriver-version=${CHROME}" \

fi

export FLASK_APP=app.py
export FLASK_DEBUG=1
python3 -m flask run -h 0.0.0.0 -p 9578 --reload

