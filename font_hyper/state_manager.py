# state_manager.py

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import traceback
import logging

logger = logging.getLogger(__name__)

class StateManager:
    """
    Handles saving and loading application state, including font categories,
    render settings, and user preferences.
    """
    def __init__(self, gui):
        self.gui = gui
        self.root = gui.root
        self.font_manager = gui.font_manager
        self.config_dir = os.path.expanduser("~/.config/font_hyper")
        self.saves_dir = os.path.join(self.config_dir, "saves")
        self.contents_file = os.path.join(self.config_dir, "contents.json")
        os.makedirs(self.saves_dir, exist_ok=True)

    def save_state(self):
        """Saves the current application state to contents.json."""
        try:
            data = self.font_manager.to_dict()
            # Save render frame settings
            data['render_text'] = self.gui.font_table_render_frame.render_entry.get()
            data['font_color'] = self.gui.font_table_render_frame.font_color

            with open(self.contents_file, 'w') as f:
                json.dump(data, f, indent=4)

            logger.debug("State saved successfully")
            #messagebox.showinfo("Success", "Settings saved successfully.")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error saving state: {str(e)}")
            messagebox.showerror("Save Error", 
                               f"An error occurred while saving state:\n{str(e)}")

    def save_state_as(self):
        """Saves the current state to a user-specified JSON file."""
        try:
            default_save_path = os.path.join(self.saves_dir, "collection_01.json")
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                initialfile="collection_01.json",
                initialdir=self.saves_dir,
                filetypes=[("JSON files", "*.json")]
            )
            
            if file_path:
                data = self.font_manager.to_dict()
                data['render_text'] = self.gui.font_table_render_frame.render_entry.get()
                data['font_color'] = self.gui.font_table_render_frame.font_color
                
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                    
                messagebox.showinfo("Success", "State saved successfully.")
                
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Save Error", f"An error occurred while saving state:\n{str(e)}")

    def load_state(self):
        """Loads application state from contents.json."""
        try:
            if os.path.exists(self.contents_file):
                with open(self.contents_file, 'r') as f:
                    data = json.load(f)
                    self.font_manager.from_dict(data)

                # Load render frame settings
                render_text = data.get('render_text', "Sample Text")
                font_color = data.get('font_color', "#000000")
                self.gui.font_table_render_frame.render_entry.delete(0, tk.END)
                self.gui.font_table_render_frame.render_entry.insert(0, render_text)
                self.gui.font_table_render_frame.font_color = font_color

                # Refresh UI
                self.gui.paths_categories_frame.update_paths_list()
                self.gui.treeview_manager.populate_font_table()
                self.gui.treeview_manager.populate_categories()

                # Rescan fonts
                self.font_manager.search_fonts()
                self.gui.treeview_manager.populate_font_table()

            else:
                logger.info("No saved state file found")
                self.font_manager.search_fonts()
                self.gui.treeview_manager.populate_font_table()
                self.gui.treeview_manager.populate_categories()
                
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error loading state: {str(e)}")
            messagebox.showerror("Load Error", 
                               f"An error occurred while loading state:\n{str(e)}")

    def load_state_from_file(self):
        """Loads application state from a user-specified JSON file."""
        try:
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                initialdir=self.saves_dir,
                filetypes=[("JSON files", "*.json")]
            )
            
            if file_path:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.font_manager.from_dict(data)
                    
                render_text = data.get('render_text', "Sample Text")
                font_color = data.get('font_color', "#000000")
                self.gui.font_table_render_frame.render_entry.delete(0, tk.END)
                self.gui.font_table_render_frame.render_entry.insert(0, render_text)
                self.gui.font_table_render_frame.font_color = font_color

                # Refresh UI components
                self.gui.paths_categories_frame.update_paths_list()
                self.gui.treeview_manager.populate_font_table()
                self.gui.treeview_manager.populate_categories()

                # Update fonts in selected category
                selected_items = self.gui.categories_treeview.selection()
                if selected_items:
                    category_label = self.gui.categories_treeview.item(selected_items[0], 'values')[2]
                    self.gui.treeview_manager.populate_fonts_in_category(category_label)
                else:
                    self.gui.treeview_manager.clear_fonts_in_category()

                # Update font notes and licenses
                for font in self.font_manager.fonts:
                    for item in self.gui.font_table_tree.get_children():
                        if self.gui.font_table_tree.set(item, "id") == font.id:
                            self.gui.font_table_tree.set(item, "user_note", font.user_note)
                            self.gui.font_table_tree.set(item, "license", font.license)

                messagebox.showinfo("Success", "State loaded successfully.")
                
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Load Error", f"An error occurred while loading state:\n{str(e)}")

    def load_state_on_startup(self):
        """Loads the initial application state when starting up."""
        try:
            if os.path.exists(self.contents_file):
                with open(self.contents_file, 'r') as f:
                    data = json.load(f)
                    self.font_manager.from_dict(data)
                    
                render_text = data.get('render_text', "Sample Text")
                font_color = data.get('font_color', "#000000")
                self.gui.font_table_render_frame.render_entry.delete(0, tk.END)
                self.gui.font_table_render_frame.render_entry.insert(0, render_text)
                self.gui.font_table_render_frame.font_color = font_color

                # Initialize UI components
                self.gui.paths_categories_frame.update_paths_list()
                self.gui.treeview_manager.populate_font_table()
                self.gui.treeview_manager.populate_categories()

                # Update font notes and licenses
                for font in self.font_manager.fonts:
                    for item in self.gui.font_table_tree.get_children():
                        if self.gui.font_table_tree.set(item, "id") == font.id:
                            self.gui.font_table_tree.set(item, "user_note", font.user_note)
                            self.gui.font_table_tree.set(item, "license", font.license)

                # Handle category selection
                selected_items = self.gui.categories_treeview.selection()
                if selected_items:
                    category_label = self.gui.categories_treeview.item(selected_items[0], 'values')[2]
                    self.gui.treeview_manager.populate_fonts_in_category(category_label)
                else:
                    self.gui.treeview_manager.clear_fonts_in_category()

            else:
                self.font_manager.search_fonts()
                self.gui.treeview_manager.populate_font_table()
                self.gui.treeview_manager.populate_categories()
                
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error loading startup state: {str(e)}")
            messagebox.showerror("Startup Load Error", 
                               f"An error occurred while loading startup state:\n{str(e)}")

    def on_exit(self):
        """Handles application exit by saving state."""
        try:
            self.save_state()
            self.root.destroy()
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error during exit: {str(e)}")
            self.root.destroy()  # Ensure application closes even if save fails
            
