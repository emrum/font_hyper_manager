# shortcuts.py
# for license info (GPL3), see license.txt from font_hyper package

import tkinter as tk
import logging
from tkinter import ttk 
from .utils import entry_field_has_focus

logger = logging.getLogger(__name__)

class ShortcutManager:
    """
    Manages keyboard shortcuts for the application.
    Centralizes all keyboard shortcuts and integrates with EventManager for actions.
    """
    def __init__(self, gui):
        self.gui = gui
        self.root = gui.root
        self.event_manager = gui.event_manager
        self.setup_shortcuts()

    def _handle_shortcut(self, event, func):
        """
        Wrapper to check focus before executing shortcut function.
        Returns 'break' to prevent default handling when shortcut is executed.
        """
        # Get currently focused widget
        focused = self.root.focus_get()
        
        # Only prevent shortcuts if an Entry widget has focus
        if isinstance(focused, (tk.Entry, ttk.Entry)):
            return
        
        # Execute the shortcut function and return 'break' to prevent default handling
        result = func(event)
        return 'break' if result != 'continue' else None

    def setup_shortcuts(self):
        """Set up all keyboard shortcuts."""
        try:
            self.bind_navigation_shortcuts()
            self.bind_control_shortcuts()
            self.bind_function_shortcuts()
            logger.debug("All shortcuts bound successfully")
        except Exception as e:
            logger.error(f"Error binding shortcuts: {str(e)}")

    def bind_navigation_shortcuts(self):
        """Bind basic navigation shortcuts."""
        evman = self.event_manager

        # Navigation bindings
        shortcuts = {
            'x': evman.focus_found_fonts_treeview,
            'c': evman.focus_categories_treeview,
            'v': evman.focus_fonts_in_category_treeview,
            'a': evman.focus_category_entry,
            's': evman.focus_search_entry,
            't': evman.focus_render_entry,
            'h': evman.toggle_hide_sys_fonts,
            'j': evman.hide_user_fonts,  # toggle 
            'm': evman.select_matching_font_on_m_key,
            'n': evman.edit_user_note_selected_font,
            'g': evman.assign_to_category,
            'r': evman.remove_font_from_category,
            'l': evman.install_category_fonts,
            'k': evman.remove_category_fonts,
            'p': evman.toggle_paths_panel,
            'u': evman.update_sys_cache_fonts,
            'z': evman.clear_search,
            'o': evman.change_category_icon, # TODO: open filedialog for category icon selection 
        }

        # Bind both lowercase and uppercase versions
        for key, func in shortcuts.items():
            def make_handler(f):
                return lambda e: self._handle_shortcut(e, f)
            
            handler = make_handler(func)
            self.root.bind(f'<{key}>', handler)
            self.root.bind(f'<{key.upper()}>', handler)

    def bind_control_shortcuts(self):
        """Bind Control key combinations."""
        evman = self.event_manager
        stman = self.gui.state_manager
        root = self.root

        def make_handler(f):
            return lambda e: self._handle_shortcut(e, f)

        # Basic control shortcuts
        root.bind('<Control-c>', make_handler(evman.copy_font_name))
        root.bind('<Control-C>', make_handler(evman.copy_font_name))

        # Shift combinations
        root.bind('<Control-Shift-C>', make_handler(evman.copy_font_path_category))
        root.bind('<Control-Shift-c>', make_handler(evman.copy_font_path_category))
        root.bind('<Control-Shift-X>', make_handler(evman.copy_and_remove_font_path_category_shortcut))
        root.bind('<Control-Shift-x>', make_handler(evman.copy_and_remove_font_path_category_shortcut))
        root.bind('<Control-Shift-V>', make_handler(evman.insert_font_from_clipboard_shortcut))
        root.bind('<Control-Shift-v>', make_handler(evman.insert_font_from_clipboard_shortcut))

        # Alt combinations
        root.bind('<Control-Alt-c>', make_handler(evman.copy_fontinfo_instance_shortcut))
        root.bind('<Control-Alt-C>', make_handler(evman.copy_fontinfo_instance_shortcut))

        # File operations
        root.bind('<Control-s>', make_handler(stman.save_state))
        root.bind('<Control-S>', make_handler(stman.save_state))
        root.bind('<Control-Shift-S>', make_handler(stman.save_state_as))
        root.bind('<Control-o>', make_handler(stman.load_state))
        root.bind('<Control-O>', make_handler(stman.load_state))
        
        # Fast navigation
        root.bind('<Control-Down>', make_handler(self.move_selection_down))
        root.bind('<Control-Up>', make_handler(self.move_selection_up))

    def bind_function_shortcuts(self):
        """Bind function key shortcuts."""
        menu = self.gui.menu_manager
        root = self.root

        def make_handler(f):
            return lambda e: self._handle_shortcut(e, f)

        # Help shortcuts
        root.bind('<F1>', make_handler(lambda e: menu.show_quick_guide()))
        root.bind('<F2>', make_handler(lambda e: menu.show_shortcuts()))
        
        # Exit binding
        root.bind('<Escape>', make_handler(lambda e: self.gui.on_exit()))

    def get_focused_treeview(self):
        """Returns the currently focused treeview widget, if any."""
        focused = self.root.focus_get()
        if isinstance(focused, ttk.Treeview):
            return focused
        return None

    def move_selection_down(self, event):
        """Move selection down by 5 items in the focused treeview."""
        treeview = self.get_focused_treeview()
        if not treeview:
            return

        try:
            items = treeview.get_children()
            if not items:
                return

            current = treeview.selection()
            if not current:
                treeview.selection_set(items[0])
                treeview.see(items[0])
                return

            current_idx = items.index(current[0])
            new_idx = min(current_idx + 5, len(items) - 1)
            new_item = items[new_idx]
            treeview.selection_set(new_item)
            treeview.focus(new_item)
            treeview.see(new_item)

        except Exception as e:
            logger.error(f"Error moving selection down: {str(e)}")

    def move_selection_up(self, event):
        """Move selection up by 5 items in the focused treeview."""
        treeview = self.get_focused_treeview()
        if not treeview:
            return

        try:
            items = treeview.get_children()
            if not items:
                return

            current = treeview.selection()
            if not current:
                treeview.selection_set(items[0])
                treeview.see(items[0])
                return

            current_idx = items.index(current[0])
            new_idx = max(current_idx - 5, 0)
            new_item = items[new_idx]
            treeview.selection_set(new_item)
            treeview.focus(new_item)
            treeview.see(new_item)

        except Exception as e:
            logger.error(f"Error moving selection up: {str(e)}")
