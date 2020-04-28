#!/bin/bash
export PYTHONPATH=$PWD

echo "Input venv name (default is venv):"
read venvname
echo "Starting virtual env."

source "$venvname/bin/activate"
pip3 install -r requirements.txt


CHROME=$(python3 bin/chrome_compatibility.py)
if [[ $CHROME -eq 0 ]]
then
    echo "Google Chrome stable and chromedriver seem compatible. No install needed."
elif [ -n $CHROME ]
then
    echo "Chromedriver seemed incompatible. Attempting install."
    pip3 install chromedriver_installer \
        --install-option="--chromedriver-version=${CHROME}" \
fi

python3 app.py
