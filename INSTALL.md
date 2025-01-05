


## linux installation 

1. install python 3  and pip, if you have not
   python -m ensurepip --upgrade
   

2. optional: if you use a python virtual environment, venv, pyenv, etc.
   edit run.sh script to activate it before starting the application, 
   else the menu entry might fail to start. 

3. optional: activate python env if required

----------------

4. install python dependencies 
   pip install -r requirements.txt
   # or start it as py module:
   python -m pip install -r requirements.txt

5. run the install script:
   sh ./install.sh
   it installs to $HOME/apps/font_hyper_manager

6. the app should appear in the menu under utility or utilities


