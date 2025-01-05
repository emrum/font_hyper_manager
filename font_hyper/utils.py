# utils.py
# for license info (GPL3), see license.txt from font_hyper package

from PIL import Image, ImageTk
import os
import logging

import tkinter as tk


logger = logging.getLogger(__name__)

def get_category_icon(image_path):
    try:
        # If no image path or invalid path, use default icon
        if not image_path or not os.path.exists(image_path):
            from .path_config import get_config_path
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
    from .path_config import get_system_paths
    system_paths = get_system_paths()
    return any(font_path.startswith(path) for path in system_paths)



def is_user_font(font_path, font_manager):
    """
    Check if font path is a user font by verifying it's not in predefined system paths.
    
    An alternative method would be: check if the fonts path is sub-path of font_manager.font_paths_user list, 
    currently it is not completely clear, what method is preferable. 
    
    Args:
        font_path (str): Path to the font file
        font_manager: FontManager instance that contains predefined paths
        
    Returns:
        bool: True if it's a user font (not in predefined paths), False otherwise
    """
    # Check if font path starts with any predefined system path
    return not any(font_path.startswith(os.path.abspath(os.path.expanduser(path))) 
                  for path in font_manager.font_paths_predefined)



def entry_field_has_focus(root):
    """Check if any Entry widget currently has focus."""
    focused = root.focus_get()
    return isinstance(focused, tk.Entry)

def focus_next(event):
    """Move focus to the next widget in tab order."""
    event.widget.tk_focusNext().focus()
    return "break"  # Prevents default handling


    
