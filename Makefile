# the variable name is the virtual environment directory
VENV := venv

# default target; no arguments
all: venv

activate: requirements.txt
	python3 -m venv $(VENV)
	mkdir $(VENV)/app/
	cp -r Makefile data/ logic/ presentation/ main.py requirements.txt $(VENV)/app
	pip install -r $(VENV)/app/requirements.txt

# venv is a shortcut target (Scripts/activate path for Windows)
venv: activate
	$(VENV)/Scripts/activate

# run the program, but first create the virtual environment and install requirements
run: venv
	cd ./$(VENV)/app/
	python main.py

# remove activation file and python cache files
clean:
	rm -rf $(VENV)
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

# run the recipes, regardless if files with same names exist
.PHONY: all venv run clean