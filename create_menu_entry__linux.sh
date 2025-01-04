#!/bin/bash

# Get the current user's home directory
USER_HOME=$(eval echo "~$USER")

# Create the .desktop file content
DESKTOP_FILE_CONTENT="[Desktop Entry]
Name=Font Hyper Manager
Exec=$USER_HOME/apps/font_hyper_manager/run.sh
Icon=$USER_HOME/apps/font_hyper_manager/font_hyper_icon.png
Type=Application
GenericName=Font Manager
Comment=python and tkinter based file manager
StartupNotify=true
Categories=Utility;Application;
"

# Write the content to the .desktop file in the user's applications directory
echo "$DESKTOP_FILE_CONTENT" > "$USER_HOME/.local/share/applications/font_hyper_manager.desktop"

echo "Desktop entry created at $USER_HOME/.local/share/applications/font_hyper_manager.desktop"


