#!/bin/bash

LOG_FILE="log.txt"


## change to directory, adjust paths 
#############################################
#$user_name = "unknown"
#cd /home/$user_name/apps/font_hyper_manager/


## setup python environment, if required 
###########################################

## Load pyenv automatically
#export PYENV_ROOT="$HOME/.pyenv"
#[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
#eval "$(pyenv init -)"


## Activate the virtual environment
#source /home/ad/path/to/venv/bin/activate
#pyenv activate envb
###########################################


# Set the environment variables
#export PYTHONPATH=$PYTHONPATH:$HOME/apps/font_hyper_manager

# Python code to execute
python_code="
import sys
sys.path.append('.')
sys.path.append('..')

import font_hyper.main_a1 as mod

# run main program
mod.main()
"

# Navigate to the directory
#cd  $HOME/apps/font_hyper_manager

# Execute the Python code and log output
python3 -c "$python_code" > $LOG_FILE 2>&1

