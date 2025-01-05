# gui_main_window.py
# for license info (GPL3), see license.txt from font_hyper package

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import logging
from .font_manager import FontManager
from .style_application import StyleManager
from .state_manager import StateManager
from .event_manager import EventManager
from .menu_setup import MenuManager
from .treeviews_and_treeview_events import TreeviewManager
from .gui_paths_categories import PathsCategoriesFrame
from .gui_font_table_render import FontTableRenderFrame
from .shortcuts import ShortcutManager
from .utils import focus_next

# Configure logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FontHyperGUI:
    """
    The main GUI class for the Font Hyper application.
    Integrates various components and manages the overall application state.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Font Hyper")
        self.root.geometry("1100x700")
        
        # Path to the icon image
        module_file = os.path.abspath(__file__)
        module_path = os.path.dirname(module_file)
        icon_path = os.path.join( module_path, "font_hyper_icon.png")
        
        # Check if the file exists
        if os.path.exists(icon_path):
            # Load the icon image
            icon = tk.PhotoImage(file=icon_path)
            
            # Set the window icon
            root.iconphoto(False, icon)
        else:
            print(f"Warning: The icon file '{icon_path}' does not exist. - FontHyperGUI.__init__")
        
        
        self.treeview_manager = None # sort of forward declaration, for setup_managers() call
        
        # Initialize managers and data
        self.setup_managers()
        self.setup_config_directories()
        
        # Initialize UI state
        self.setup_ui_state()
        
        # Create base frames
        self.create_base_frames()
        
        # Setup UI components
        self.setup_ui()
        self.toggle_top_row()
        
        # Create treeview manager after UI setup
        self.treeview_manager = TreeviewManager(self)

        # Load state and bind window close
        self.state_manager.load_state_on_startup()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Load initial data
        self.initial_data_load()

        self.style_manager.setup_styles()


    def setup_managers(self):
        """Initialize all manager classes."""
        self.font_manager = FontManager()
        self.style_manager = StyleManager(self)
        self.state_manager = StateManager(self)
        self.event_manager = EventManager(self)
        self.menu_manager = MenuManager(self)
        self.shortcut_manager = ShortcutManager(self)  # Add this line


    def setup_config_directories(self):
        """Sets up necessary configuration directories."""
        from .path_config import get_config_path
        self.config_dir = get_config_path()
        self.saves_dir = os.path.join(self.config_dir, "saves")
        self.contents_file = os.path.join(self.config_dir, "contents.json")
        os.makedirs(self.saves_dir, exist_ok=True)

    def setup_ui_state(self):
        """Initialize UI state variables."""
        self.selected_fonts = []
        self.selected_category = None
        self.top_row_visible = True
        self.fonts_in_category_mapping = {}
        self.category_icons = {}

    def create_base_frames(self):
        """Creates the basic frame structure needed by managers."""
        # Configure root window
        self.root.rowconfigure(0, weight=0, minsize=120)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # First row frame
        self.first_row_frame = ttk.Frame(self.root)
        self.first_row_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.first_row_frame.columnconfigure(0, weight=1)

        # Main PanedWindow
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned_window.grid(row=1, column=0, sticky="nsew")

        # Upper and Lower panes
        self.upper_pane = ttk.Frame(self.paned_window)
        self.lower_pane = ttk.Frame(self.paned_window)
        self.paned_window.add(self.upper_pane, weight=1)
        self.paned_window.add(self.lower_pane, weight=3)

        # Set default height for upper pane
        self.paned_window.sashpos(0, 90)

        # Configure upper pane layout
        self.setup_upper_pane()
        
        # Configure lower pane layout
        self.setup_lower_pane()

    def setup_upper_pane(self):
        """Configure the upper pane layout."""
        self.upper_pane.rowconfigure(0, weight=1)
        self.upper_pane.columnconfigure(0, weight=1)
        self.upper_pane.columnconfigure(1, weight=0)
        self.upper_pane.columnconfigure(2, weight=0)

        # Create main frames
        self.categories_frame = ttk.LabelFrame(self.upper_pane, text="Categories", width=180)
        self.categories_frame.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)
        self.categories_frame.rowconfigure(0, weight=1)
        self.categories_frame.columnconfigure(0, weight=1)

        self.category_actions_frame = ttk.LabelFrame(self.upper_pane, text="Category Actions", width=120)
        self.category_actions_frame.grid(row=0, column=2, sticky="nsew", padx=4, pady=4)

    def setup_lower_pane(self):
        """Configure the lower pane layout."""
        self.lower_pane.rowconfigure(0, weight=2)
        self.lower_pane.columnconfigure(0, weight=2)

        # Create nested PanedWindow
        self.lower_paned_window = ttk.PanedWindow(self.lower_pane, orient=tk.HORIZONTAL)
        self.lower_paned_window.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

        # Create main frames
        self.font_table_frame = ttk.LabelFrame(self.lower_paned_window, text="Found Fonts Table (FFT)")
        self.lower_paned_window.add(self.font_table_frame, weight=3)
        self.font_table_frame.rowconfigure(0, weight=0)
        self.font_table_frame.rowconfigure(1, weight=1)
        self.font_table_frame.columnconfigure(0, weight=1)

        self.fonts_in_category_frame = ttk.LabelFrame(self.lower_paned_window, text="Fonts in Category (FIC)")
        self.lower_paned_window.add(self.fonts_in_category_frame, weight=2)
        self.fonts_in_category_frame.rowconfigure(0, weight=1)
        self.fonts_in_category_frame.columnconfigure(0, weight=1)

    def setup_ui(self):
        """Sets up the main user interface components."""
        # Setup first row with paths and categories
        self.paths_categories_frame = PathsCategoriesFrame(
            self.first_row_frame, self.font_manager, self)
        self.paths_categories_frame.grid(row=0, column=0, sticky="nsew")

        # Setup Render Frame in upper pane
        self.font_table_render_frame = FontTableRenderFrame(
            self.upper_pane, self.font_manager, self)
        self.font_table_render_frame.grid(
            row=0, column=0, sticky="nsew", padx=(4, 4), pady=4)

        # Setup category actions
        self.setup_category_actions()

        # Setup search bar
        self.setup_search_bar()




    def setup_category_actions(self):
        """Sets up category action buttons and entry field."""
        from .utils import focus_next
        
        # Category Entry Frame
        category_entry_frame = ttk.Frame(self.category_actions_frame)
        category_entry_frame.pack(fill=tk.X, padx=5, pady=(4, 2))

        ttk.Label(category_entry_frame, text="Category Name:").pack(anchor='w', padx=5, pady=2)
        self.edit_category_entry = ttk.Entry(category_entry_frame, width=12)
        self.edit_category_entry.pack(fill=tk.X, padx=2, pady=2)
        self.edit_category_entry.bind("<Return>", focus_next)  # Add focus_next binding
        

        # Category Buttons
        buttons = [
            ("New Category", self.event_manager.add_category, 'button_cat'),
            ("Delete Category", self.paths_categories_frame.delete_category, 'button_cat'),
            ("Insert Font\nin Category", self.event_manager.assign_to_category, 'button_font'),
            ("Remove Font\nfrom Category", self.event_manager.remove_font_from_category, 'button_font'),
            ("Install Category", self.event_manager.install_category_fonts, 'button_inst'),
            ("Uninstall Category", self.event_manager.remove_category_fonts, 'button_inst'),
            ("Update Sys Cache", self.event_manager.update_sys_cache_fonts, 'button_sys')
        ]

        for text, command, style in buttons:
            btn = ttk.Button(self.category_actions_frame, text=text, 
                           command=command, style=f'{style}.TButton')
            btn.pack(fill=tk.X, padx=2, pady=2)


    def setup_search_bar(self):
        """Sets up the search bar within the font table frame."""
        from .utils import focus_next
        
        search_frame = ttk.Frame(self.font_table_frame)
        search_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Search components
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=2, pady=2)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=2, pady=2, sticky="we")
        self.search_entry.bind("<KeyRelease>", self.event_manager.filter_fonts)
        self.search_entry.bind("<Return>", focus_next)  # Add focus_next binding

        # Buttons
        buttons = [
            ("Clear Text", self.event_manager.clear_search),
            ("Hide Sys Fonts", self.event_manager.toggle_hide_sys_fonts),
            ("Hide User Fonts", self.event_manager.hide_user_fonts)
        ]

        for col, (text, command) in enumerate(buttons, start=2):
            btn = ttk.Button(search_frame, text=text, command=command)
            btn.grid(row=0, column=col, padx=2, pady=2)
            if text == "Hide Sys Fonts":
                self.hide_sys_fonts_button = btn
            elif text == "Hide User Fonts":
                self.hide_user_fonts_button = btn

        search_frame.columnconfigure(1, weight=1)



    def toggle_top_row(self):
        """Toggles the visibility of the top row containing font paths."""
        logger.debug(f"Toggle top row called. Current visibility: {self.top_row_visible}")
        
        # Toggle visibility state
        self.top_row_visible = not self.top_row_visible
        
        # Synchronize with menu state
        self.menu_manager.paths_visible.set(self.top_row_visible)
        
        if not self.top_row_visible:
            self.root.grid_rowconfigure(0, minsize=1, weight=0)
            self.first_row_frame.grid_remove()
        else:
            self.root.grid_rowconfigure(0, minsize=120, weight=0)
            self.first_row_frame.grid()
            
        # Update button text in FontTableRenderFrame
        new_text = "Hide Paths" if self.top_row_visible else "Show Paths"
        if hasattr(self, 'font_table_render_frame') and hasattr(self.font_table_render_frame, 'toggle_top_row_button'):
            self.font_table_render_frame.toggle_top_row_button.config(text=new_text)
            
        logger.debug(f"Visibility after toggle: {self.top_row_visible}")
        self.root.update_idletasks()
        

    def initial_data_load(self):
        """Performs initial font search and populates treeviews."""
        self.font_manager.search_fonts()
        self.treeview_manager.populate_font_table()
        self.treeview_manager.populate_categories()

    def on_exit(self):
        """Handle application exit."""
        self.state_manager.save_state()
        self.root.destroy()

    # Delegate methods to event_manager
    def copy_font_name(self):
        self.event_manager.copy_font_name()

    def copy_font_path(self):
        self.event_manager.copy_font_path()

    def copy_font_name_category(self):
        self.event_manager.copy_font_name_category()

    def copy_font_path_category(self):
        self.event_manager.copy_font_path_category()

    def copy_and_remove_font_path_category(self):
        self.event_manager.copy_and_remove_font_path_category_shortcut(None)

    def insert_font_from_clipboard(self):
        self.event_manager.insert_font_from_clipboard()

    # Access properties for convenience
    @property
    def categories_treeview(self):
        return self.treeview_manager.categories_treeview

    @property
    def font_table_tree(self):
        return self.treeview_manager.font_table_tree

    @property
    def fonts_in_category_tree(self):
        return self.treeview_manager.fonts_in_category_tree

            
    def get_category_icon(self, image_path):
        """
        Gets a category icon, delegating to the utils function.
        Maintains a reference to prevent garbage collection.
        """
        from .utils import get_category_icon
        icon = get_category_icon(image_path)
        self.category_icons[image_path] = icon  # Keep reference to prevent garbage collection
        return icon

    def save_category_icon_reference(self, category_id, icon):
        """Save a reference to a category icon to prevent garbage collection."""
        self.category_icons[category_id] = icon


            


        
