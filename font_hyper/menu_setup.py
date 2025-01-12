import tkinter as tk
import logging
from .dialogs import ScrollableDialog
from tkinter import messagebox
import os

logger = logging.getLogger(__name__)

class MenuManager:
    """
    Manages the application's menu structure and commands.
    Integrates with EventManager and StateManager.
    """
    def __init__(self, gui):
        self.gui = gui
        self.root = gui.root
        self.event_manager = gui.event_manager
        self.state_manager = gui.state_manager
        self.setup_menu()

    def setup_menu(self):
        """Set up the main menu bar and all submenus."""
        try:
            menubar = tk.Menu(self.root)
            
            # Create and add all menus
            menubar.add_cascade(label="File", menu=self.create_file_menu(menubar))
            menubar.add_cascade(label="View", menu=self.create_view_menu(menubar))
            menubar.add_cascade(label="Categories", menu=self.create_categories_menu(menubar))
            menubar.add_cascade(label="Tools", menu=self.create_tools_menu(menubar))
            menubar.add_cascade(label="Help", menu=self.create_help_menu(menubar))
            
            # Set the menubar
            self.root.config(menu=menubar)
            logger.debug("Menu system initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up menu: {str(e)}")
            raise


    def create_file_menu(self, menubar):
        """Create the File menu."""
        menu = tk.Menu(menubar, tearoff=0)
        
        # State management
        menu.add_command(label="Save State (Ctrl+S)", 
                        command=self.state_manager.save_state)
        menu.add_command(label="Save State As... (Ctrl+Shift+S)", 
                        command=self.state_manager.save_state_as)
        menu.add_command(label="Load State (Ctrl+O)", 
                        command=self.state_manager.load_state)
        menu.add_command(label="Load State From File...", 
                        command=self.state_manager.load_state_from_file)
        menu.add_separator()
        
        # Font scanning
        menu.add_command(label="Rescan Font Paths", 
                        command=lambda: self.gui.font_manager.search_fonts)
        menu.add_separator()
        
        # Exit
        menu.add_command(label="Exit (Esc)", command=self.gui.on_exit)
        
        return menu


    def create_view_menu(self, menubar):
        """Create the View menu."""
        menu = tk.Menu(menubar, tearoff=0)
        
        # View toggles
        self.paths_visible = tk.BooleanVar(value=False)
        menu.add_checkbutton(label="Show Paths Panel (P)",
                            variable=self.paths_visible,
                            command=self.toggle_paths_panel)
        
        # Filter options
        menu.add_separator()
        menu.add_command(label="Hide System Fonts (H)",
                        command=self.event_manager.toggle_hide_sys_fonts)
        menu.add_command(label="Hide User Fonts (J)",
                        command=self.event_manager.hide_user_fonts)
        menu.add_command(label="Clear Filters (Z)",
                        command=self.event_manager.clear_search)
        
        return menu
        
        

    def create_categories_menu(self, menubar):
        """Create the Categories menu."""
        menu = tk.Menu(menubar, tearoff=0)
        
        menu.add_command(label="New Category (A)",
                        command=self.event_manager.add_category)
        menu.add_command(label="Delete Selected Category",
                        command=lambda: self.gui.paths_categories_frame.delete_category)
        menu.add_separator()
        menu.add_command(label="Install Category Fonts (L)",
                        command=self.event_manager.install_category_fonts)
        menu.add_command(label="Remove Category Fonts (K)",
                        command=self.event_manager.remove_category_fonts)
        
        return menu
        


    def create_tools_menu(self, menubar):
        """Create the Tools menu."""
        menu = tk.Menu(menubar, tearoff=0)
        
        menu.add_command(label="Update System Font Cache (U)",
                        command=self.event_manager.update_sys_cache_fonts)
        menu.add_separator()
        menu.add_command(label="Export Category List",
                        command=self.export_category_list)
        menu.add_command(label="Export Font List",
                        command=self.export_font_list)
        
        menu.add_separator()
        menu.add_command(label="Add System Default Paths",
                        command=self.add_system_default_paths)
        menu.add_command(label="Clear System Paths List",
                        command=self.clear_system_paths)
        
        return menu
        


    def create_help_menu(self, menubar):
        """Create the Help menu."""
        menu = tk.Menu(menubar, tearoff=0)
        
        menu.add_command(label="Quick Guide (F1)", command=self.show_quick_guide)
        menu.add_command(label="Keyboard Shortcuts (F2)", command=self.show_shortcuts)
        menu.add_separator()
        menu.add_command(label="About Font Hyper", command=self.show_about)
        
        return menu


    def toggle_paths_panel(self):
        """Toggle the visibility of the paths panel."""
        try:
            # Update the menu's checkbox state
            self.paths_visible.set(not self.paths_visible.get())
            # Call the main window's toggle function
            self.gui.toggle_top_row()
            logger.debug(f"Paths panel visibility toggled via menu: {self.paths_visible.get()}")
        except Exception as e:
            logger.error(f"Error toggling paths panel from menu: {str(e)}")
            


    def show_quick_guide(self):
        """Show the quick guide dialog."""
        text = """
Quick Guide to Font Hyper:

1. Adding Fonts
   - Use 'Add Path' to add font directories
   - Click 'Scan for Fonts' to update the font list

2. Managing Categories
   - Create categories to organize fonts
   - Select fonts and use 'Insert Font in Category'
   - Install/uninstall entire categories at once

3. Font Preview
   - Select any font to preview it
   - Adjust size with the slider
   - Change text and color as needed

4. Installation
   - Use category installation buttons
   - Update system cache after changes
   - Check installation status in category list

5. Search and Filter
   - Use the search box to find fonts
   - Toggle system/user font visibility
   - Clear filters to see all fonts

For more details, check the keyboard shortcuts guide!
"""
        dialog = ScrollableDialog(self.root)
        dialog.show("Quick Guide", text)

    def show_shortcuts(self):
        """Show the keyboard shortcuts dialog."""
        text = """
Keyboard Shortcuts:

Navigation:
X - Focus Found Fonts treeview
C - Focus Categories treeview
V - Focus Fonts in Category treeview
A - Focus category entry field
S - Focus search field
T - Focus render text field
Ctrl+Up/Down - Move selection up/down by 5 items

Font Management:
G - Insert selected font into category
R - Remove selected font from category
M - Match font in Found Fonts list
N - Edit user note for selected font
O - Change category icon
L - Install category fonts
K - Uninstall category fonts

View Controls:
H - Toggle system fonts visibility
J - Toggle user fonts visibility
P - Toggle paths panel
Z - Clear search filters
U - Update font cache

File Operations:
Ctrl+S - Save state
Ctrl+Shift+S - Save state as
Ctrl+O - Load state
Esc - Exit application

Clipboard Operations:
Ctrl+C - Copy font name
Ctrl+Shift+C - Copy font path from category
Ctrl+Shift+X - Cut font from category
Ctrl+Shift+V - Paste font into category
Ctrl+Alt+C - Copy font info as JSON

Help:
F1 - Quick Guide
F2 - Keyboard Shortcuts
"""
        dialog = ScrollableDialog(self.root)
        dialog.show("Keyboard Shortcuts", text)

    def show_about(self):
        """Show the about dialog."""
        text = """
Font Hyper Manager

Version: 2025.01.04
A powerful font management tool for Linux systems.

Features:
- Font organization with categories
- Preview with custom text and size
- System and user font management
- Category-based installation
- Advanced search and filtering

Created with Python and Tkinter.
License: GPL-3.0
"""
        dialog = ScrollableDialog(self.root)
        dialog.show("About Font Hyper", text)

    def export_category_list(self):
        """Export the list of categories and their fonts."""
        try:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Category List"
            )
            
            if not filepath:
                return

            with open(filepath, 'w') as f:
                for category_label, category in self.gui.font_manager.categories.items():
                    f.write(f"\nCategory: {category_label}\n")
                    f.write("-" * 50 + "\n")
                    for font_path in category.fonts_list:
                        f.write(f"  - {os.path.basename(font_path)}\n")

            logger.info(f"Category list exported to: {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting category list: {str(e)}")
            messagebox.showerror("Export Error", 
                               f"Failed to export category list: {str(e)}")



    def export_font_list(self):
        """Export the complete list of fonts."""
        try:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Font List"
            )
            
            if not filepath:
                return

            with open(filepath, 'w') as f:
                f.write("Font List\n")
                f.write("=" * 50 + "\n\n")
                for font in sorted(self.gui.font_manager.fonts, key=lambda x: x.font_name):
                    f.write(f"Name: {font.font_name}\n")
                    f.write(f"Style: {font.font_style}\n")
                    f.write(f"File: {font.font_file}\n")
                    if font.user_note:
                        f.write(f"Note: {font.user_note}\n")
                    f.write("-" * 30 + "\n")

            logger.info(f"Font list exported to: {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting font list: {str(e)}")
            messagebox.showerror("Export Error", 
                               f"Failed to export font list: {str(e)}")




    def add_system_default_paths(self):
        """Add the default system font paths to predefined paths."""
        try:
            from .path_config import get_system_paths
            
            # Get system-specific paths
            system_paths = get_system_paths()
            paths_added = 0
            
            # Get current predefined paths for comparison
            current_paths = set(self.gui.font_manager.font_paths_predefined)
            
            # Add each path if it's not already in the predefined paths
            for path in system_paths:
                if path not in current_paths and os.path.exists(path):
                    if path not in self.gui.font_manager.font_paths_predefined:
                        self.gui.font_manager.font_paths_predefined.append(path)
                        # Update the predefined paths list in the UI
                        self.gui.paths_categories_frame.predefined_list.insert(tk.END, path)
                        paths_added += 1
            
            if paths_added > 0:
                # Scan for fonts after adding paths
                self.gui.font_manager.search_fonts()
                self.gui.treeview_manager.populate_font_table()
                
                logger.info(f"Added {paths_added} system default font paths to predefined paths")
                messagebox.showinfo("Success", 
                                  f"Added {paths_added} system default paths to predefined paths and updated the font list.")
            else:
                messagebox.showinfo("Info", "All system default paths are already added to predefined paths.")
                
        except Exception as e:
            logger.error(f"Error adding system default paths: {str(e)}")
            messagebox.showerror("Error", 
                               f"Failed to add system default paths:\n{str(e)}")

    def clear_system_paths(self):
        """Clear all paths from the predefined paths list."""
        try:
            # Ask for confirmation
            confirm = messagebox.askyesno("Confirm Clear", 
                                        "Are you sure you want to clear all predefined system paths?")
            if not confirm:
                return

            # Clear the paths from font manager
            self.gui.font_manager.font_paths_predefined.clear()
            
            # Clear the UI list
            self.gui.paths_categories_frame.predefined_list.delete(0, tk.END)
            
            # Update fonts
            self.gui.font_manager.search_fonts()
            self.gui.treeview_manager.populate_font_table()
            
            logger.info("Cleared all predefined system paths")
            messagebox.showinfo("Success", "All predefined system paths have been cleared.")
            
        except Exception as e:
            logger.error(f"Error clearing system paths: {str(e)}")
            messagebox.showerror("Error", 
                               f"Failed to clear system paths:\n{str(e)}")
                               
                               


