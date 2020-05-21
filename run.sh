#!/bin/bash
export PYTHONPATH=$PWD

echo "Input venv name (default is venv):"
#read venvname
echo "Starting virtual env."

source "newv/bin/activate"
pip3 install -r requirements.txt

CHROME=$(python3 bin/chrome_compatibility.py --check 2>&1 >/dev/null)
echo $CHROME
if [[ $CHROME -eq 0 ]]
then
    echo "Google Chrome stable and chromedriver seem compatible. No install needed."
fi

if [[ -n $CHROME ]]
then
    echo "Chromedriver seemed incompatible. Attempting installi of $CHROME."
    python3 bin/chrome_compatibility.py --install
    python3 chromedriver_installer/setup.py install --chromedriver-version=$CHROME
fi

export FLASK_APP=app.py
export FLASK_DEBUG=1
python3 -m flask run -h 0.0.0.0 -p 9578 --reload
