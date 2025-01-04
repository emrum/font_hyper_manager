import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import traceback
import os
import logging

logger = logging.getLogger(__name__)

class PathsCategoriesFrame(ttk.Frame):
    """
    Frame managing the predefined and user-defined font paths.
    Integrates with EventManager and StateManager for operations.
    """
    def __init__(self, parent, font_manager, main_window):
        super().__init__(parent)
        self.font_manager = font_manager
        self.main_window = main_window
        self.event_manager = main_window.event_manager
        self.state_manager = main_window.state_manager
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface components."""
        self.columnconfigure(0, weight=1, uniform="path_columns")
        self.columnconfigure(1, weight=1, uniform="path_columns")
        self.columnconfigure(2, weight=0)

        # Predefined Paths Frame
        self.setup_predefined_paths_frame()
        
        # User Paths Frame
        self.setup_user_paths_frame()
        
        # Path Actions Frame
        self.setup_path_actions_frame()

    def setup_predefined_paths_frame(self):
        """Sets up the predefined paths section."""
        predefined_frame = ttk.LabelFrame(self, text="Predefined Paths", padding=(4, 4))
        predefined_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        predefined_frame.columnconfigure(0, weight=1)
        predefined_frame.rowconfigure(1, weight=1)

        self.predefined_list = tk.Listbox(predefined_frame, height=5, selectmode=tk.SINGLE)
        self.predefined_list.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Add scrollbar
        self.setup_listbox_scrollbar(predefined_frame, self.predefined_list)

        for path in self.font_manager.font_paths_predefined:
            self.predefined_list.insert(tk.END, path)

    def setup_user_paths_frame(self):
        """Sets up the user paths section."""
        user_frame = ttk.LabelFrame(self, text="User Paths", padding=(4, 4))
        user_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        user_frame.columnconfigure(0, weight=1)
        user_frame.rowconfigure(1, weight=1)

        self.user_list = tk.Listbox(user_frame, height=5, selectmode=tk.MULTIPLE)
        self.user_list.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Add scrollbar
        self.setup_listbox_scrollbar(user_frame, self.user_list)

        for path in self.font_manager.font_paths_user:
            self.user_list.insert(tk.END, path)

    def setup_path_actions_frame(self):
        """Sets up the path actions section."""
        path_actions_frame = ttk.LabelFrame(self, text="Path Actions", padding=(4, 4), width=160)
        path_actions_frame.grid(row=0, column=2, sticky="ns", padx=5, pady=5)
        path_actions_frame.grid_propagate(False)
        path_actions_frame.columnconfigure(0, weight=1)

        # Action buttons
        self.add_user_path_btn = ttk.Button(path_actions_frame, text="Add Path", 
                                          command=self.add_user_path)
        self.add_user_path_btn.pack(fill=tk.X, padx=5, pady=(10, 5))

        self.remove_user_path_btn = ttk.Button(path_actions_frame, text="Remove Path", 
                                             command=self.remove_user_path)
        self.remove_user_path_btn.pack(fill=tk.X, padx=5, pady=5)

        self.scan_fonts_btn = ttk.Button(path_actions_frame, text="Scan for Fonts", 
                                       command=self.scan_for_fonts)
        self.scan_fonts_btn.pack(fill=tk.X, padx=5, pady=(5, 10))

    def setup_listbox_scrollbar(self, parent, listbox):
        """Adds a scrollbar to a listbox."""
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        listbox.configure(yscrollcommand=scrollbar.set)

    def add_user_path(self):
        """Opens a dialog to add a new user-defined font path."""
        try:
            path = filedialog.askdirectory()
            if path:
                valid, invalid = self.font_manager.verify_paths([path])
                if valid:
                    if valid[0] not in self.font_manager.font_paths_user:
                        self.font_manager.font_paths_user.append(valid[0])
                        self.user_list.insert(tk.END, valid[0])
                        self.font_manager.search_fonts()
                        self.main_window.treeview_manager.populate_font_table()
                        logger.info(f"Added user path: {valid[0]}")
                    else:
                        messagebox.showinfo("Info", "Path already added.")
                else:
                    messagebox.showwarning("Invalid Path", f"The path {path} does not exist.")
        except Exception as e:
            logger.error(f"Error adding user path: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while adding the path:\n{str(e)}")

    def remove_user_path(self):
        """Removes the selected user-defined font paths."""
        try:
            selected = self.user_list.curselection()
            if not selected:
                messagebox.showwarning("Selection Error", "No user font path selected.")
                return

            for index in reversed(selected):
                path = self.user_list.get(index)
                if path in self.font_manager.font_paths_user:
                    self.font_manager.font_paths_user.remove(path)
                    self.user_list.delete(index)
                    logger.info(f"Removed user path: {path}")

            self.font_manager.fonts.clear()
            self.font_manager.search_fonts()
            self.main_window.treeview_manager.populate_font_table()
            
        except Exception as e:
            logger.error(f"Error removing user path: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while removing the path:\n{str(e)}")

    def scan_for_fonts(self):
        """Initiates a font scan across all paths."""
        try:
            self.font_manager.search_fonts()
            self.main_window.treeview_manager.populate_font_table()
            logger.info("Font scan completed")
            messagebox.showinfo("Success", "Font scan completed successfully.")
        except Exception as e:
            logger.error(f"Error scanning for fonts: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while scanning for fonts:\n{str(e)}")

    def delete_category(self):
        """Removes the selected category."""
        try:
            selected_items = self.main_window.categories_treeview.selection()
            if not selected_items:
                messagebox.showwarning("Selection Error", "No category selected.")
                return

            for item in selected_items:
                values = self.main_window.categories_treeview.item(item, 'values')
                _, _, category_label, _ = values
                if category_label in self.font_manager.categories:
                    uninstall = messagebox.askyesno("Uninstall Fonts",
                                                  "Do you want to uninstall category fonts before deleting?")
                    if uninstall:
                        self.event_manager.remove_category_fonts()

                    confirm = messagebox.askyesno("Confirm Deletion",
                                               f"Delete category '{category_label}', are you sure?")
                    if confirm:
                        del self.font_manager.categories[category_label]
                        self.main_window.categories_treeview.delete(item)
                        logger.info(f"Removed category: {category_label}")
                else:
                    messagebox.showwarning("Warning", f"Category '{category_label}' does not exist.")

        except Exception as e:
            logger.error(f"Error removing category: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while removing the category:\n{str(e)}")

    def update_paths_list(self):
        """Refreshes both predefined and user paths lists."""
        try:
            self.predefined_list.delete(0, tk.END)
            self.user_list.delete(0, tk.END)

            for path in self.font_manager.font_paths_predefined:
                self.predefined_list.insert(tk.END, path)

            for path in self.font_manager.font_paths_user:
                self.user_list.insert(tk.END, path)
                
            logger.debug("Paths lists updated")
            
        except Exception as e:
            logger.error(f"Error updating paths lists: {str(e)}")
            messagebox.showerror("Update Error", f"An error occurred while updating paths:\n{str(e)}")
            
