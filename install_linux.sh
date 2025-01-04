##!/usr/bin/bash


# install config files
cp -dpr  config/font_hyper_conf  ~/.config/


# install main application module
mkdir ~/apps
mkdir ~/apps/font_hyper_manager
cp -dpr  ./*  ~/apps/font_hyper_manager


## install menu entry
mkdir ~/.local/share/applications 
#cp  -dp  font_hyper_manager.desktop ~/.local/share/applications/
#xdg-desktop-menu  install font_hyper_manager.desktop  --novendor 

./create_menu_entry__linux.sh


# create a desktop icon 
# xdg-desktop-icon install  font_hyper_manager.desktop   --novendor

