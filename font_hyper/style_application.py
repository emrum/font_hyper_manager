# style_application.py

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import logging

logger = logging.getLogger(__name__)

class StyleManager:
    """
    Manages application styles and appearance.
    
    Responsible for:
    - Setting up the application's visual theme
    - Managing treeview styles (regular and large font)
    - Handling focus styles for different treeviews
    - Configuring button styles
    - Managing font configurations
    """
    def __init__(self, gui):
        """
        Initialize the StyleManager.
        
        Args:
            gui: The main GUI instance containing all widgets
        """
        self.gui = gui
        self.style = ttk.Style()
        self.setup_styles()

    def setup_styles(self):
        """
        Set up all application styles.
        
        Configures:
        - Base treeview styles
        - Focus handling styles
        - Large font styles for special treeviews
        - Button styles
        - Header styles
        """
        try:
            # Get default font for base configuration
            default_font = tkFont.nametofont("TkDefaultFont")
            
            # Set up base styles
            self.setup_base_treeview_style(default_font)
            
            # Set up regular treeview focus styles
            self.setup_regular_focus_styles(default_font)
            
            # Set up large font styles
            self.setup_large_font_styles(default_font)
            
            # Configure tag styles for bold text
            self.setup_tag_styles()
            
            # Set up button styles
            self.setup_button_styles()
            
            logger.debug("All styles configured successfully")
            
        except Exception as e:
            logger.error(f"Error setting up styles: {str(e)}")
            raise

    def setup_base_treeview_style(self, default_font):
        """
        Configure the base treeview style settings.
        
        Args:
            default_font: The default font to use for the treeview
        """
        # Base Treeview style
        self.style.configure("Treeview", 
                           rowheight=20,
                           font=default_font,
                           background="white",
                           foreground="black",
                           fieldbackground="white")
        
        # Fix treeview layout for icon alignment
        self.style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        # Treeview header style
        self.style.configure("Treeview.Heading",
                           font=default_font,
                           foreground='black',
                           background='#f0f0f0')
                           
        # Selection colors
        self.style.map('Treeview',
                      foreground=[('selected', 'white')],
                      background=[('selected', '#0078d7')])

    def setup_regular_focus_styles(self, default_font):
        """
        Configure focus styles for regular treeviews.
        
        Args:
            default_font: The default font to use
        """
        # Focused state
        self.style.configure("Focused.Treeview", 
                           font=default_font,
                           rowheight=20,
                           background="#f8ebca",
                           foreground="black",
                           fieldbackground="#f8ebca")
        
        # Unfocused state
        self.style.configure("Unfocused.Treeview", 
                           font=default_font,
                           rowheight=20,
                           background="white",
                           foreground="black",
                           fieldbackground="white")

    def setup_large_font_styles(self, default_font):
        """
        Configure styles for large font treeviews.
        
        Args:
            default_font: The base font to derive the large font from
        """
        # Create large font
        large_font = default_font.copy()
        large_font.configure(size=default_font.cget("size") + 4)
        
        # Base large font style
        self.style.configure("LargeFont.Treeview", 
                           font=large_font, 
                           rowheight=34,
                           background="white",
                           foreground="black",
                           fieldbackground="white",
                           padding=(4, 4))

        # Large font focus styles
        self.style.configure("LargeFont.Focused.Treeview", 
                           background="#f8ebca",
                           foreground="black",
                           fieldbackground="#f8ebca",
                           font=large_font,
                           rowheight=34,
                           padding=(4, 4))
        
        self.style.configure("LargeFont.Unfocused.Treeview", 
                           background="white",
                           foreground="black",
                           fieldbackground="white",
                           font=large_font,
                           rowheight=34,
                           padding=(4, 4))

    def setup_tag_styles(self):
        """Configure styles for text tags (e.g., bold text)."""
        self.style.configure("Bold.Treeview", 
                           font=('TkDefaultFont', 13, 'bold'))

    def setup_button_styles(self):
        """
        Configure styles for different types of buttons.
        
        Defines color schemes for:
        - Category buttons
        - Font operation buttons
        - Installation buttons
        - System operation buttons
        """
        button_styles = {
            'button_cat': '#D5C0C0',   # Category operations
            'button_font': '#eeee8d',   # Font operations
            'button_inst': '#dfc9dd',   # Installation operations
            'button_sys': '#c8d9d8'     # System operations
        }

        for style_name, bg_color in button_styles.items():
            self.style.configure(f'{style_name}.TButton', 
                               background=bg_color)
            self.style.map(f'{style_name}.TButton',
                         background=[('active', '#d6d6d6')],
                         foreground=[('active', 'black')])

    def on_treeview_focus_in(self, treeview):
        """
        Handle focus-in event for treeviews.
        
        Args:
            treeview: The treeview widget receiving focus
        """
        try:
            current_style = treeview.cget('style')
            if 'LargeFont' in current_style:
                treeview.configure(style="LargeFont.Focused.Treeview")
            else:
                treeview.configure(style="Focused.Treeview")
            
            logger.debug(f"Treeview focus in - Applied style: {treeview.cget('style')}")
            
        except Exception as e:
            logger.error(f"Error in treeview focus in: {str(e)}")

    def on_treeview_focus_out(self, treeview):
        """
        Handle focus-out event for treeviews.
        
        Args:
            treeview: The treeview widget losing focus
        """
        try:
            current_style = treeview.cget('style')
            if 'LargeFont' in current_style:
                treeview.configure(style="LargeFont.Unfocused.Treeview")
            else:
                treeview.configure(style="Unfocused.Treeview")
            
            logger.debug(f"Treeview focus out - Applied style: {treeview.cget('style')}")
            
        except Exception as e:
            logger.error(f"Error in treeview focus out: {str(e)}")
#
