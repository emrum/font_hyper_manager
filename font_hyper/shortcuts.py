import tkinter as tk
import logging
from tkinter import ttk 
from .utils import entry_field_has_focus

logger = logging.getLogger(__name__)

class ShortcutManager:
    """
    Manages keyboard shortcuts for the application.
    Integrates with EventManager for actions.
    """
    def __init__(self, gui):
        self.gui = gui
        self.root = gui.root
        self.event_manager = gui.event_manager
        self.bind_all_shortcuts()

    def bind_all_shortcuts(self):
        """Set up all keyboard shortcuts."""
        try:
            # Navigation shortcuts (with both lowercase and uppercase)
            self.bind_navigation_shortcuts()
            
            # Control key combinations
            self.bind_control_shortcuts()
            
            # Function keys
            self.bind_function_shortcuts()
            
            logger.debug("All shortcuts bound successfully")
            
        except Exception as e:
            logger.error(f"Error binding shortcuts: {str(e)}")

    def bind_navigation_shortcuts(self):
        """Bind basic navigation shortcuts."""
        navigation_bindings = {
            'x': self.focus_found_fonts,
            'c': self.focus_categories,
            'v': self.focus_fonts_in_category,
            'a': self.focus_category_entry,
            's': self.focus_search,
            't': self.focus_render_text,
            'h': self.toggle_hide_sys_fonts,
            'm': self.select_matching_font,
            'n': self.edit_user_note,
            'g': self.insert_to_category,
            'r': self.remove_from_category,
            'o': self.change_category_icon,
            'l': self.install_category,
            'k': self.uninstall_category,
            'p': self.toggle_paths_panel,
            'u': self.update_font_cache,
            'z': self.clear_search,
            'j': self.toggle_user_fonts
        }

        # Bind both lowercase and uppercase
        for key, func in navigation_bindings.items():
            self.root.bind(f'<{key}>', func)
            self.root.bind(f'<{key.upper()}>', func)

    def bind_control_shortcuts(self):
        """Bind Control key combinations."""
        # Basic control shortcuts
        self.root.bind('<Control-c>', self.copy_font_name)
        self.root.bind('<Control-C>', self.copy_font_name)

        # Shift combinations
        self.root.bind('<Control-Shift-C>', self.copy_font_path_category)
        self.root.bind('<Control-Shift-c>', self.copy_font_path_category)
        self.root.bind('<Control-Shift-X>', self.cut_font_from_category)
        self.root.bind('<Control-Shift-x>', self.cut_font_from_category)
        self.root.bind('<Control-Shift-V>', self.paste_font_to_category)
        self.root.bind('<Control-Shift-v>', self.paste_font_to_category)

        # Alt combinations
        self.root.bind('<Control-Alt-c>', self.copy_fontinfo)
        self.root.bind('<Control-Alt-C>', self.copy_fontinfo)

        # File operations
        self.root.bind('<Control-s>', lambda e: self.gui.state_manager.save_state())
        self.root.bind('<Control-S>', lambda e: self.gui.state_manager.save_state())
        self.root.bind('<Control-Shift-S>', lambda e: self.gui.state_manager.save_state_as())
        self.root.bind('<Control-o>', lambda e: self.gui.state_manager.load_state())
        self.root.bind('<Control-O>', lambda e: self.gui.state_manager.load_state())
        
        # Fast navigation
        self.root.bind('<Control-Down>', self.move_selection_down)
        self.root.bind('<Control-Up>', self.move_selection_up)

    def bind_function_shortcuts(self):
        """Bind function key shortcuts."""
        # Help shortcuts
        self.root.bind('<F1>', lambda e: self.show_quick_guide(e))
        self.root.bind('<F2>', lambda e: self.show_shortcuts(e))
        
        # Exit binding
        self.root.bind('<Escape>', lambda e: self.gui.on_exit())

    # Help Functions
    def show_quick_guide(self, event=None):
        """Show the quick guide dialog."""
        if entry_field_has_focus(self.root):
            return
        self.gui.menu_manager.show_quick_guide()

    def show_shortcuts(self, event=None):
        """Show the keyboard shortcuts dialog."""
        if entry_field_has_focus(self.root):
            return
        self.gui.menu_manager.show_shortcuts()

    # Navigation Functions
    def focus_found_fonts(self, event):
        """Focus the Found Fonts treeview."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.focus_found_fonts_treeview(event)

    def focus_categories(self, event):
        """Focus the Categories treeview."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.focus_categories_treeview(event)

    def focus_fonts_in_category(self, event):
        """Focus the Fonts in Category treeview."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.focus_fonts_in_category_treeview(event)

    def focus_category_entry(self, event):
        """Focus the category entry field."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.focus_category_entry(event)

    def focus_search(self, event):
        """Focus the search entry field."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.focus_search_entry(event)

    def focus_render_text(self, event):
        """Focus the render text entry field."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.focus_render_entry(event)

    # Action Functions
    def toggle_hide_sys_fonts(self, event):
        """Toggle system fonts visibility."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.toggle_hide_sys_fonts(event)

    def select_matching_font(self, event):
        """Select matching font in the font table."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.select_matching_font_on_m_key(event)

    def edit_user_note(self, event):
        """Edit user note for selected font."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.edit_user_note_selected_font(event)

    def insert_to_category(self, event):
        """Insert selected font to category."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.assign_to_category()

    def remove_from_category(self, event):
        """Remove selected font from category."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.remove_font_from_category()

    def change_category_icon(self, event):
        """Change the icon of the selected category."""
        if entry_field_has_focus(self.root):
            return
        selected = self.gui.categories_treeview.selection()
        if selected:
            self.gui.treeview_manager.select_category_icon(selected[0])

    def install_category(self, event):
        """Install fonts from the selected category."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.install_category_fonts()

    def uninstall_category(self, event):
        """Uninstall fonts from the selected category."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.remove_category_fonts()

    def toggle_paths_panel(self, event):
        """Toggle the visibility of the paths panel."""
        if entry_field_has_focus(self.root):
            return
        self.gui.menu_manager.toggle_paths_panel()

    def update_font_cache(self, event):
        """Update the system font cache."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.update_sys_cache_fonts()

    def clear_search(self, event):
        """Clear the search field and filters."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.clear_search()

    def toggle_user_fonts(self, event):
        """Toggle visibility of user fonts."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.hide_user_fonts()

    # Clipboard Functions
    def copy_font_name(self, event):
        """Copy selected font name."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.copy_font_name()

    def copy_font_path_category(self, event):
        """Copy font path from category."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.copy_font_path_category()

    def cut_font_from_category(self, event):
        """Cut font from category."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.copy_and_remove_font_path_category_shortcut(event)

    def paste_font_to_category(self, event):
        """Paste font to category."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.insert_font_from_clipboard_shortcut(event)

    def copy_fontinfo(self, event):
        """Copy font info as JSON."""
        if entry_field_has_focus(self.root):
            return
        self.event_manager.copy_fontinfo_instance_shortcut(event)



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

            # Get current selection
            current = treeview.selection()
            if not current:
                treeview.selection_set(items[0])
                treeview.see(items[0])
                return

            # Find current index
            current_idx = items.index(current[0])
            # Calculate new index
            new_idx = min(current_idx + 5, len(items) - 1)
            # Select and show new item
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

            # Get current selection
            current = treeview.selection()
            if not current:
                treeview.selection_set(items[0])
                treeview.see(items[0])
                return

            # Find current index
            current_idx = items.index(current[0])
            # Calculate new index
            new_idx = max(current_idx - 5, 0)
            # Select and show new item
            new_item = items[new_idx]
            treeview.selection_set(new_item)
            treeview.focus(new_item)
            treeview.see(new_item)

        except Exception as e:
            logger.error(f"Error moving selection up: {str(e)}")
            
        
#
