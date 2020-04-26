#!/bin/bash
export PYTHONPATH=$PWD

echo "Input venv name (default is venv):"
read venvname
echo "Starting virtual env."

#readonly sourcefile="./$venvname/bin/activate"
#source ${sourcefile}

source "$venvname/bin/activate"
# pip3 install -r requirements.txt


CHROME=$(python3 bin/chrome_compatibility.py)
if [[ $CHROME -eq 0 ]]
then
    echo "Google Chrome stable and chromedriver seem compatible. No install needed."
elif [ -n $CHROME ]
then
    echo "Chromedriver seemed incompatible. Attempting install."
    pip3 install chromedriver_installer \
        --install-option="--chromedriver-version=81.0.4044.69" \
        --install-option="--chromedriver-checksums=11bc281b27db997b5045b376866b8ed5"
fi

python3 app.py
