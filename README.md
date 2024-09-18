# DBT project, Ball Balancing Robot (Curiosum)

We are using Python virtual environment for development throughout the project. All the dependencies are defined in requirements.txt file, which ensures that everybody works with the same versions of dependencies. 

As for now, we have a single global virtual environment for the entire repo.

## Prerequisites

# Python version
Ensure that you use python3. Preferable version Python 3.11.2, but later versions should also be okay.

# Pip
Pip3 should be installed, if not, install with:

sudo apt update
sudo apt install python3-pip
pip3 --version (verify version)


## First setup:

# Creating environment
python3 -m venv dbt-venv (Linux)
python -m venv dbt-venv (Windows)

# Activating environment
source dbt-venv/bin/activate (Linux)
.\venv\Scripts\activate (Windows)

# Installing dependencies
pip install -r requirements.txt


## Everyday usage
Once virtual environment is created and dependencies are installed, you can follow the steps:

# Activate environment
source dbt-venv/bin/activate (Linux)
.\venv\Scripts\activate (Windows)

# Run applications within the environmet
python3 my_app.py (Linux)
python my_app.py (Windows)

# Deactivate environment
deactivate

## Updating dependencies
If there is a need to update the dependencies, add the new dependency to requirement.txt file.

# Update dependencies manually (Preferrable)
Add dependency on the new line in requirements.txt

# Update dependencies automatically
Otherwise, if you install the new dependency with
pip install new-dependency

add the new dependency to requirements.txt with
pip freeze > requirements.txt

OBS! Make sure to not att the dependencies that are not used/needed, if you intalled some now unused dependency before!

Don't forget to commit and push in the end of the day.

