# add venv folder to -gitignore
if ! grep -q ".flavours-env/" .gitignore; then
  echo "" >> .gitignore
  echo "# Flavours Font Editor Python Virtual Environment" >> .gitignore
  echo ".flavours-env/" >> .gitignore
fi

# create venv
virtualenv --system-site-packages .flavours-env

# activate
source .flavours-env/bin/activate

# install requirements
if test -f requirements.txt; then
    pip3 install -r requirements.txt
fi

# modify Python’s Info.plist
python3 `python3 -c "import flavours; import os; print(os.path.dirname(flavours.__file__))"`/hack.py change

# run IDE
python3 `python3 -c "import flavours; import os; print(os.path.dirname(flavours.__file__))"`/app.py

# modify Python’s Info.plist
python3 `python3 -c "import flavours; import os; print(os.path.dirname(flavours.__file__))"`/hack.py revert

# quite
deactivate
