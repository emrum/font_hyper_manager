# utils.py
# for license info (GPL3), see license.txt from font_hyper package

from PIL import Image, ImageTk
import os
import logging

import tkinter as tk


logger = logging.getLogger(__name__)

def get_category_icon(image_path):
    """
    Loads and returns a PhotoImage for the category icon.
    If the category has no valid image, it uses 'cat_icon.png' from the script directory.
    Returns a PhotoImage that can be used in tkinter widgets.
    """
    try:
        # If no image path or invalid path, use default icon
        if not image_path or not os.path.exists(image_path):
            default_icon_path = os.path.join(os.path.dirname(__file__), 'cat_icon.png')
            if os.path.exists(default_icon_path):
                image = Image.open(default_icon_path)
                image = image.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                return photo
            else:
                logger.warning(f"Default category icon not found at {default_icon_path}")
                # Create transparent image if default icon not found
                default_icon = Image.new('RGBA', (32, 32), (255, 255, 255, 0))
                return ImageTk.PhotoImage(default_icon)
        
        # Load provided image
        image = Image.open(image_path)
        image = image.resize((32, 32), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
        
    except Exception as e:
        logger.error(f"Error loading category icon: {e}")
        # Return transparent image on error
        default_icon = Image.new('RGBA', (32, 32), (255, 255, 255, 0))
        return ImageTk.PhotoImage(default_icon)

def is_system_font(font_path):
    """Check if font path is in system directories."""
    system_paths = ['/usr/share/fonts', '/usr/local/share/fonts']
    return any(font_path.startswith(path) for path in system_paths)

def is_user_font(font_path):
    """Check if font path is in user's home directory."""
    home_dir = os.path.expanduser('~')
    return font_path.startswith(home_dir)

def entry_field_has_focus(root):
    """Check if any Entry widget currently has focus."""
    focused = root.focus_get()
    return isinstance(focused, tk.Entry)

def focus_next(event):
    """Move focus to the next widget in tab order."""
    event.widget.tk_focusNext().focus()
    return "break"  # Prevents default handling


    
