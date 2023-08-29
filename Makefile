# the variable name is the virtual environment directory
VENV := venv

# default target; no arguments
all: $(VENV)

venv: main.py data/ logic/ presentation/
	python3 -m venv $(VENV)
	$(VENV)/Scripts/activate
	mkdir $(VENV)/app/
	cp -r data/ logic/ presentation/ main.py requirements.txt $(VENV)/app
	pip install -r $(VENV)/app/requirements.txt

run: venv
	python3 $(VENV)/app/main.py

# remove virtual environment and all files within it
clean:
	rm -rf $(VENV)

# run the recipes, regardless if files with same names exist
.PHONY: all venv clean run