# event_manager.py
# for license info (GPL3), see license.txt from font_hyper package

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import traceback
import logging
import subprocess
import json
from .dialogs import ScrollableDialog

logger = logging.getLogger(__name__)

class EventManager:
    """
    Centralizes event handling for the application, including menu events,
    button actions, and treeview interactions.
    """
    def __init__(self, gui):
        self.gui = gui
        self.root = gui.root
        self.font_manager = gui.font_manager

    # Focus Events
    def focus_found_fonts_treeview(self, event=None):
        """Focuses the Found Fonts Treeview."""
        if self.gui.font_table_tree.get_children():
            selected = self.gui.font_table_tree.selection()
            item = selected[0] if selected else self.gui.font_table_tree.get_children()[0]
            self.gui.font_table_tree.focus_set()
            self.gui.font_table_tree.focus(item)
            self.gui.font_table_tree.selection_set(item)
            self.gui.font_table_tree.see(item)
        return "break"

    def focus_category_entry(self, event=None):
        self.gui.edit_category_entry.focus_set()
        return "break"

    def focus_categories_treeview(self, event=None):
        if self.gui.categories_treeview.get_children():
            selected = self.gui.categories_treeview.selection()
            item = selected[0] if selected else self.gui.categories_treeview.get_children()[0]
            self.gui.categories_treeview.focus_set()
            self.gui.categories_treeview.focus(item)
            self.gui.categories_treeview.selection_set(item)
            self.gui.categories_treeview.see(item)
        return "break"

    def focus_fonts_in_category_treeview(self, event=None):
        if self.gui.fonts_in_category_tree.get_children():
            selected = self.gui.fonts_in_category_tree.selection()
            item = selected[0] if selected else self.gui.fonts_in_category_tree.get_children()[0]
            self.gui.fonts_in_category_tree.focus_set()
            self.gui.fonts_in_category_tree.focus(item)
            self.gui.fonts_in_category_tree.selection_set(item)
            self.gui.fonts_in_category_tree.see(item)
        return "break"

    def focus_search_entry(self, event=None):
        self.gui.search_entry.focus_set()
        return "break"

    def focus_render_entry(self, event=None):
        self.gui.font_table_render_frame.render_entry.focus_set()
        return "break"

    def toggle_paths_panel(self, event=None):
        """Toggles the visibility of the paths panel."""
        current_state = self.gui.menu_manager.paths_visible.get()
        self.gui.menu_manager.paths_visible.set(not current_state)
        self.gui.toggle_top_row()
        return "break"

    # Clipboard Operations
    def copy_font_name(self, event=None):
        """Copies selected font name to clipboard."""
        selected = self.gui.font_table_tree.selection()
        if selected:
            font_name = self.gui.font_table_tree.set(selected[0], "font_name")
            self.root.clipboard_clear()
            self.root.clipboard_append(font_name)
            messagebox.showinfo("Copied", f"Font Name '{font_name}' copied to clipboard.")
        else:
            messagebox.showwarning("No Selection", "No font selected to copy name.")
        return "break"

    def copy_font_path(self, event=None):
        """Copies selected font path to clipboard."""
        selected = self.gui.font_table_tree.selection()
        if selected:
            font_path = self.gui.font_table_tree.set(selected[0], "font_path")
            self.root.clipboard_clear()
            self.root.clipboard_append(font_path)
            messagebox.showinfo("Copied", "Font Path copied to clipboard.")
        else:
            messagebox.showwarning("No Selection", "No font selected to copy path.")
        return "break"

    def copy_font_name_category(self, event=None):
        """Copies selected font name from category to clipboard."""
        selected = self.gui.fonts_in_category_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "No font selected to copy name.")
            return "break"

        font_file = self.gui.fonts_in_category_tree.set(selected[0], "font_file")
        font_info = next((f for f in self.font_manager.fonts if f.font_file == font_file), None)
        
        if font_info:
            self.root.clipboard_clear()
            self.root.clipboard_append(font_info.font_name)
            messagebox.showinfo("Copied", f"Font Name '{font_info.font_name}' copied to clipboard.")
        else:
            messagebox.showwarning("Not Found", "Selected font information not found.")
        return "break"

    def copy_font_path_category(self, event=None):
        """Copies selected font path from category to clipboard."""
        selected = self.gui.fonts_in_category_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "No font selected to copy path.")
            return "break"

        font_file = self.gui.fonts_in_category_tree.set(selected[0], "font_file")
        font_info = next((f for f in self.font_manager.fonts if f.font_file == font_file), None)
        
        if font_info:
            self.root.clipboard_clear()
            self.root.clipboard_append(font_info.font_path)
            messagebox.showinfo("Copied", "Font Path copied to clipboard.")
        else:
            messagebox.showwarning("Not Found", "Selected font information not found.")
        return "break"

    # Category Operations
    def add_category(self, event=None):
        """Adds a new category based on user input."""
        category_label = self.gui.edit_category_entry.get().strip()
        if category_label:
            if category_label not in self.font_manager.categories:
                self.font_manager.add_category(category_label)
                count = 0
                icon = self.gui.get_category_icon(
                    self.font_manager.categories[category_label].image_path)
                category_id = self.font_manager.categories[category_label].idx
                self.gui.categories_treeview.insert(
                    '',
                    'end',
                    image=icon,
                    values=(count, "", category_label, category_id)
                )
                self.gui.category_icons[category_id] = icon
                self.gui.edit_category_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Info", "Category already exists.")
        else:
            messagebox.showwarning("Input Error", "Category name cannot be empty.")
        return "break"

    def assign_to_category(self, event=None):
        """Assigns selected fonts to the selected category."""
        selected_fonts = self.gui.treeview_manager.get_selected_fonts()
        category_label = self.gui.treeview_manager.get_selected_category()

        if not selected_fonts:
            messagebox.showwarning("Selection Error", "No fonts selected.")
            return "break"
        if not category_label:
            messagebox.showwarning("Selection Error", "No category selected.")
            return "break"

        try:
            selected_category_items = self.gui.categories_treeview.selection()
            if not selected_category_items:
                messagebox.showwarning("Selection Error", "No category selected.")
                return "break"

            selected_category_item = selected_category_items[0]
            category_values = self.gui.categories_treeview.item(selected_category_item, 'values')
            category_id = category_values[3]

            self.font_manager.assign_fonts_to_category(category_label, selected_fonts)
            self.gui.treeview_manager.populate_fonts_in_category(category_label)
            self.gui.treeview_manager.update_category_count(category_label)
            self.font_manager.update_category_info(category_label)
            self.gui.treeview_manager.populate_categories()

            new_category_item = self.gui.treeview_manager.get_category_item_by_id(category_id)
            if new_category_item:
                self.gui.categories_treeview.selection_set(new_category_item)
                self.gui.categories_treeview.focus(new_category_item)
                self.gui.categories_treeview.see(new_category_item)

            messagebox.showinfo("Success", 
                            f"Assigned {len(selected_fonts)} fonts to category '{category_label}'.")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error assigning fonts: {str(e)}")
            messagebox.showerror("Assignment Error", 
                             f"An error occurred while assigning fonts:\n{str(e)}")
        return "break"

    def remove_font_from_category(self, event=None):
        """Removes selected font from the current category."""
        selected_category_items = self.gui.categories_treeview.selection()
        if not selected_category_items:
            messagebox.showwarning("Selection Error", "Select a category first.")
            return "break"

        selected_category_item = selected_category_items[0]
        selected_font_items = self.gui.fonts_in_category_tree.selection()
        
        if not selected_font_items:
            messagebox.showwarning("Selection Error", 
                               "Select a font to remove from the category.")
            return "break"

        font_item = selected_font_items[0]
        all_current_fonts = self.gui.fonts_in_category_tree.get_children()
        try:
            current_index = all_current_fonts.index(font_item)
            preceding_index = max(min(current_index - 1, len(all_current_fonts) - 1), 0)
        except ValueError:
            preceding_index = 0

        try:
            values = self.gui.categories_treeview.item(selected_category_item, 'values')
            category_label = values[2]
            category_id = values[3]

            font_file = self.gui.fonts_in_category_tree.set(font_item, "font_file")
            font_info = next((f for f in self.font_manager.fonts if f.font_file == font_file), None)

            if not font_info:
                messagebox.showerror("Error", 
                                 f"Font '{font_file}' not found in the main font table.")
                return "break"

            category = self.font_manager.categories.get(category_label)
            if not category or font_info.font_path not in category.fonts_list:
                messagebox.showwarning("Warning",
                                   f"Font '{font_file}' is not associated with "
                                   f"category '{category_label}'.")
                return "break"

            category.fonts_list.remove(font_info.font_path)
            self.gui.treeview_manager.populate_fonts_in_category(category_label)
            self.gui.treeview_manager.update_category_count(category_label)
            self.font_manager.update_category_info(category_label)
            self.gui.treeview_manager.populate_categories()

            new_category_item = self.gui.treeview_manager.get_category_item_by_id(category_id)
            if new_category_item:
                self.gui.categories_treeview.selection_set(new_category_item)
                self.gui.categories_treeview.focus(new_category_item)
                self.gui.categories_treeview.see(new_category_item)

            def restore_font_selection():
                new_font_items = self.gui.fonts_in_category_tree.get_children()
                if new_font_items:
                    safe_index = min(preceding_index, len(new_font_items) - 1)
                    new_selected_item = new_font_items[safe_index]
                    self.gui.fonts_in_category_tree.selection_set(new_selected_item)
                    self.gui.fonts_in_category_tree.focus(new_selected_item)
                    self.gui.fonts_in_category_tree.see(new_selected_item)

            self.gui.fonts_in_category_tree.after(60, restore_font_selection)

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error removing font: {str(e)}")
            messagebox.showerror("Removal Error", 
                             f"An error occurred while removing the font:\n{str(e)}")
        return "break"

    # Category Font Installation Operations
    def install_category_fonts(self, event=None):
        """Installs all fonts in the selected category."""
        from .path_config import get_install_path
        
        category_label = self.gui.treeview_manager.get_selected_category()
        if not category_label:
            messagebox.showwarning("Selection Error", "No category selected.")
            return "break"

        category = self.font_manager.categories.get(category_label)
        if not category:
            messagebox.showwarning("Category Error", "Invalid category selected.")
            return "break"

        try:
            fonts_dir = os.path.expanduser(get_install_path())
            os.makedirs(fonts_dir, exist_ok=True)

            installed_count = 0
            for font_path in category.fonts_list:
                if os.path.exists(font_path):
                    dest_path = os.path.join(fonts_dir, os.path.basename(font_path))
                    if not os.path.exists(dest_path):
                        os.symlink(font_path, dest_path)
                        installed_count += 1

            if installed_count > 0:
                category.is_installed = True
                selected_items = self.gui.categories_treeview.selection()
                if selected_items:
                    item = selected_items[0]
                    values = list(self.gui.categories_treeview.item(item, 'values'))
                    values[1] = "@"
                    self.gui.categories_treeview.item(item, values=tuple(values), tags=('bold',))
                
                self.gui.treeview_manager.update_category_count(category_label)
                messagebox.showinfo("Success", 
                        f"Installed {installed_count} fonts from category '{category_label}'.")
            else:
                messagebox.showinfo("Info", "No new fonts to install in this category.")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error installing fonts: {str(e)}")
            messagebox.showerror("Installation Error", 
                             f"An error occurred while installing fonts:\n{str(e)}")
        return "break"

    def remove_category_fonts(self, event=None):
        """Uninstalls all fonts in the selected category."""
        from .path_config import get_install_path
        
        category_label = self.gui.treeview_manager.get_selected_category()
        if not category_label:
            messagebox.showwarning("Selection Error", "No category selected.")
            return "break"

        category = self.font_manager.categories.get(category_label)
        if not category:
            messagebox.showwarning("Category Error", "Invalid category selected.")
            return "break"

        try:
            fonts_dir = os.path.expanduser(get_install_path())
            removed_count = 0
            for font_path in category.fonts_list:
                dest_path = os.path.join(fonts_dir, os.path.basename(font_path))
                if os.path.exists(dest_path) and os.path.islink(dest_path):
                    os.unlink(dest_path)
                    removed_count += 1

            if removed_count > 0:
                category.is_installed = False
                selected_items = self.gui.categories_treeview.selection()
                if selected_items:
                    item = selected_items[0]
                    values = list(self.gui.categories_treeview.item(item, 'values'))
                    values[1] = ""  # Clear "Inst" column
                    self.gui.categories_treeview.item(item, values=tuple(values), tags=())
                
                self.gui.treeview_manager.update_category_count(category_label)
                messagebox.showinfo("Success", 
                                f"Removed {removed_count} fonts from category '{category_label}'.")
            else:
                messagebox.showinfo("Info", "No installed fonts found in this category.")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error removing fonts: {str(e)}")
            messagebox.showerror("Removal Error", 
                             f"An error occurred while removing fonts:\n{str(e)}")
        return "break"

    def update_sys_cache_fonts(self, event=None):
        """Updates the system font cache using fc-cache command."""
        try:
            wait_window = tk.Toplevel(self.root)
            wait_window.transient(self.root)
            wait_window.title("Updating Font Cache")
            
            window_width = 300
            window_height = 100
            screen_width = self.root.winfo_x() + self.root.winfo_width()//2
            screen_height = self.root.winfo_y() + self.root.winfo_height()//2
            x = screen_width - window_width//2
            y = screen_height - window_height//2
            wait_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
            
            wait_window.configure(padx=20, pady=20)
            wait_window.resizable(False, False)
            wait_window.grab_set()
            
            message = ttk.Label(wait_window, text="Updating font cache, please wait...")
            message.pack(expand=True)
            
            def run_update():
                try:
                    process = subprocess.run(['fc-cache', '-fv'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE, 
                                        text=True)
                    
                    wait_window.destroy()
                    
                    text_dialog = ScrollableDialog(self.root)
                    if process.returncode == 0:
                        text_dialog.show("System - Font Cache Update - Report", 
                                     "Success:\n" + process.stdout)
                    else:
                        text_dialog.show("System - Font Cache Update - Report", 
                                     "Error:\n" + process.stderr)
                        
                except Exception as e:
                    wait_window.destroy()
                    logger.error(f"Error updating font cache: {str(e)}")
                    messagebox.showerror("Error", 
                                     f"An error occurred while updating font cache:\n{str(e)}")
            
            self.root.after(100, run_update)
            
        except Exception as e:
            logger.error(f"Error setting up font cache update: {str(e)}")
            messagebox.showerror("Error", 
                             f"An error occurred while setting up font cache update:\n{str(e)}")
        return "break"

    # Search and Filter Operations
    def filter_fonts(self, event=None):
        """Handles filtering of fonts based on search text and flags."""
        try:
            query = self.gui.search_entry.get().lower()

            logger.debug(f"Filtering fonts with query='{query}', "
                      f"hide_sys_fonts_flag={getattr(self.gui, 'hide_sys_fonts_flag', False)}, "
                      f"hide_user_fonts_flag={getattr(self.gui, 'hide_user_fonts_flag', False)}")

            self.gui.font_table_tree.delete(*self.gui.font_table_tree.get_children())

            matching_fonts = 0
            for font in self.font_manager.fonts:
                font_name = font.font_name.lower()
                font_file = font.font_file.lower()
                font_path = font.font_path.lower()

                from .utils import is_system_font, is_user_font
                is_sys_font = is_system_font(font_path)
                is_user = is_user_font(font_path, self.font_manager)

                should_hide = False
                if getattr(self.gui, 'hide_sys_fonts_flag', False) and is_sys_font:
                    should_hide = True
                if getattr(self.gui, 'hide_user_fonts_flag', False) and is_user:
                    should_hide = True

                if query and query not in font_name and query not in font_file and query not in font_path:
                    should_hide = True

                if not should_hide:
                    self.gui.font_table_tree.insert('', 'end', values=(
                        font.font_name,
                        font.font_style,
                        font.user_note,
                        font.license,
                        font.font_file,
                        font.font_path,
                        font.id
                    ))
                    matching_fonts += 1

            logger.debug(f"Found {matching_fonts} matching fonts after filtering")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error filtering fonts: {str(e)}")
        return "break"

    def clear_search(self, event=None):
        """Clears the search entry and resets filters."""
        self.gui.search_entry.delete(0, tk.END)
        self.filter_fonts()
        return "break"

    def toggle_hide_sys_fonts(self, event=None):
        """Toggles visibility of system fonts."""
        self.gui.hide_sys_fonts_flag = not getattr(self.gui, 'hide_sys_fonts_flag', False)
        new_text = "Show Sys Fonts" if self.gui.hide_sys_fonts_flag else "Hide Sys Fonts"
        self.gui.hide_sys_fonts_button.config(text=new_text)
        self.filter_fonts()
        return "break"

    def hide_user_fonts(self, event=None):
        """Toggles visibility of user fonts."""
        self.gui.hide_user_fonts_flag = not getattr(self.gui, 'hide_user_fonts_flag', False)
        new_text = "Show User Fonts" if self.gui.hide_user_fonts_flag else "Hide User Fonts"
        self.gui.hide_user_fonts_button.config(text=new_text)
        self.filter_fonts()
        return "break"

    # Selection and Note Editing
    def select_matching_font_on_m_key(self, event=None):
        """Handles 'm' key press for matching fonts between views."""
        selected = self.gui.fonts_in_category_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "No font selected in Fonts-in-Category to match.")
            return "break"

        selected_item = selected[0]
        font_file = self.gui.fonts_in_category_tree.set(selected_item, "font_file")
        
        found = False
        for item in self.gui.font_table_tree.get_children():
            table_font_file = self.gui.font_table_tree.set(item, "font_file")
            if table_font_file == font_file:
                self.gui.font_table_tree.see(item)
                self.gui.font_table_tree.selection_set(item)
                self.gui.font_table_tree.focus(item)
                found = True
                break
        
        if not found:
            messagebox.showwarning("No Match", 
                               f"Could not find font file '{font_file}' in the font table. "
                               "Try rescanning your font paths.")

        self.gui.fonts_in_category_tree.focus_set()
        self.gui.fonts_in_category_tree.selection_set(selected_item)
        self.gui.fonts_in_category_tree.see(selected_item)
        return "break"

    def edit_user_note_selected_font(self, event=None):
        """Handles user note editing for selected font."""
        selected = self.gui.font_table_tree.selection()
        if selected:
            item = selected[0]
            bbox = self.gui.font_table_tree.bbox(item, "user_note")
            if bbox:
                x, y, width, height = bbox
                dummy_event = tk.Event()
                dummy_event.x = x + width // 2
                dummy_event.y = y + height // 2
                self.gui.treeview_manager.on_double_click_font_table(dummy_event)
        else:
            messagebox.showwarning("No Selection", "No font selected to edit user note.")
        return "break"

    # Clipboard Shortcut Handlers
    def copy_font_name_shortcut(self, event=None):
        """Handles Ctrl+C shortcut for copying font name."""
        self.copy_font_name()
        return "break"

    def copy_font_path_category_shortcut(self, event=None):
        """Handles Ctrl+Shift+C shortcut for copying category font path."""
        self.copy_font_path_category()
        return "break"

    def copy_and_remove_font_path_category_shortcut(self, event=None):
        """Handles Ctrl+Shift+X shortcut for cutting font from category."""
        selected = self.gui.fonts_in_category_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "No font selected to copy and remove.")
            return "break"

        font_file = self.gui.fonts_in_category_tree.set(selected[0], "font_file")
        font_info = next((f for f in self.font_manager.fonts if f.font_file == font_file), None)
        
        if font_info:
            self.root.clipboard_clear()
            self.root.clipboard_append(font_info.font_path)
            self.remove_font_from_category()
        else:
            messagebox.showerror("Error", "Selected font information not found.")
        return "break"

    def insert_font_from_clipboard_shortcut(self, event=None):
        """Handles Ctrl+Shift+V shortcut for pasting font into category."""
        self.insert_font_from_clipboard()
        return "break"

    def insert_font_from_clipboard(self):
        """Inserts a new font path from the clipboard into fonts_in_category_tree."""
        try:
            clipboard_content = self.root.clipboard_get().strip()
            if not clipboard_content:
                messagebox.showwarning("Clipboard Empty", "Clipboard does not contain any font path.")
                return "break"

            if not os.path.exists(clipboard_content):
                messagebox.showerror("Invalid Path", f"The font path '{clipboard_content}' does not exist.")
                return "break"

            category_label = self.gui.treeview_manager.get_selected_category()
            if not category_label:
                messagebox.showwarning("No Category Selected", "Please select a category to insert the font.")
                return "break"

            category = self.font_manager.categories.get(category_label)
            if not category:
                messagebox.showerror("Category Error", f"Category '{category_label}' does not exist.")
                return "break"

            if clipboard_content in category.fonts_list:
                messagebox.showinfo("Already Exists", "The font is already present in the selected category.")
                return "break"

            font_info = self.font_manager.get_font_info_by_path(clipboard_content)
            if not font_info:
                font_info = self.font_manager.add_font(clipboard_content)

            self.font_manager.assign_fonts_to_category(category_label, [font_info])
            self.gui.treeview_manager.populate_fonts_in_category(category_label)
            self.gui.treeview_manager.update_category_count(category_label)

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error inserting font from clipboard: {str(e)}")
            messagebox.showerror("Insertion Error", 
                             f"An error occurred while inserting the font:\n{str(e)}")
        return "break"

    def copy_fontinfo_instance_shortcut(self, event=None):
        """Handles Ctrl+Alt+C shortcut for copying FontInfo instance."""
        selected = self.gui.font_table_tree.selection()
        if selected:
            font_id = self.gui.font_table_tree.set(selected[0], "id")
            font_info = next((f for f in self.font_manager.fonts if f.id == font_id), None)
            if font_info:
                font_info_dict = font_info.to_dict()
                font_info_json = json.dumps(font_info_dict, indent=4)
                self.root.clipboard_clear()
                self.root.clipboard_append(font_info_json)
                messagebox.showinfo("Copied", f"FontInfo instance for '{font_info.font_name}' copied to clipboard.")
            else:
                messagebox.showerror("Error", "FontInfo instance not found.")
        else:
            messagebox.showwarning("No Selection", "No font selected to copy FontInfo instance.")
        return "break"

    def change_category_icon(self, event=None):
        """Change icon for the selected category."""
        selected_items = self.gui.categories_treeview.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "No category selected.")
            return "break"
        
        item = selected_items[0]
        self.gui.treeview_manager.select_category_icon(item)
        # or: self.gui.treeview_manager.show_icon_selection_menu  ??
        return "break"

    def get_selected_fonts(self):
        """Get selected FontInfo objects from the font table tree."""
        try:
            selected = self.gui.font_table_tree.selection()
            fonts = []
            for item in selected:
                values = self.gui.font_table_tree.item(item, 'values')
                font_id = values[6]  # "id" is the 7th column
                font = next((f for f in self.font_manager.fonts if f.id == font_id), None)
                if font:
                    fonts.append(font)
            return fonts
        except Exception as e:
            logger.error(f"Error getting selected fonts: {str(e)}")
            return []

    def get_selected_category(self):
        """Get the currently selected category label."""
        try:
            selected = self.gui.categories_treeview.selection()
            if not selected:
                return None
            return self.gui.categories_treeview.item(selected[0], 'values')[2]
        except Exception as e:
            logger.error(f"Error getting selected category: {str(e)}")
            return None
            
            
            
