# treeviews_and_treeview_events.py
# for license info (GPL3), see license.txt from font_hyper package

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import logging
import traceback
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)

class TreeviewManager:
    """
    Manages all treeviews in the application, handling their creation,
    population, and event bindings. Integrates with EventManager and StateManager.
    """
    def __init__(self, gui):
        self.gui = gui
        self.root = gui.root
        self.font_manager = gui.font_manager
        self.style_manager = gui.style_manager
        self.event_manager = gui.event_manager
        self.state_manager = gui.state_manager
        
        self.fonts_in_category_mapping = {}
        self._default_icon = None  # Hold reference to default icon
        
        # Load default icon
        self.load_default_icon()
        
        # Set up treeviews
        self.setup_font_table_tree()
        self.setup_categories_treeview()
        self.setup_fonts_in_category_tree()


    def setup_font_table_tree(self):
        """Set up the main font table treeview."""
        columns = [
            ("font_name", "Font Name", 150),
            ("font_style", "Font Style", 100),
            ("user_note", "User Note", 200),
            ("license", "License", 150),
            ("font_file", "Font File", 150),
            ("font_path", "Font Path", 200),
            ("id", "Id", 0)
        ]

        # Create and configure the Treeview
        self.font_table_tree = ttk.Treeview(
            self.gui.font_table_frame,
            columns=[col[0] for col in columns],
            show='headings',
            selectmode='extended'
        )

        # Configure columns
        for col, text, width in columns:
            self.font_table_tree.heading(col, text=text)
            self.font_table_tree.column(col, width=width, anchor=tk.W, stretch=False)

        # Hide ID column
        self.font_table_tree.column("id", width=0, stretch=False)

        # Setup scrollbars
        self.setup_scrollbars_FFT(self.gui.font_table_frame, self.font_table_tree, 
                            show_horizontal=True)

        # Grid layout
        self.font_table_tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Context Menu
        self.setup_font_table_context_menu()

        # Bind events
        self.bind_font_table_events()

        # Set default style without focus changes
        self.font_table_tree.configure(style="Treeview")  # Use default style



    def setup_fonts_in_category_tree(self):
        """Set up the fonts in category treeview."""
        self.fonts_in_category_tree = ttk.Treeview(
            self.gui.fonts_in_category_frame,
            columns=("font_name_style", "found_it", "font_file"),
            show='headings',
            selectmode='browse'
        )

        # Configure headings and columns
        self.fonts_in_category_tree.heading("font_name_style", text="Font Name / Style")
        self.fonts_in_category_tree.heading("found_it", text="Found it")
        self.fonts_in_category_tree.heading("font_file", text="Font File")
        
        # Update column widths and configuration
        self.fonts_in_category_tree.column("font_name_style", width=200, anchor='w', stretch=True)
        self.fonts_in_category_tree.column("found_it", width=60, anchor=tk.CENTER, stretch=False)
        self.fonts_in_category_tree.column("font_file", width=0, anchor='w', stretch=False) # width 0, invisible

        # Setup scrollbars
        vsb = ttk.Scrollbar(self.gui.fonts_in_category_frame, orient="vertical", 
                           command=self.fonts_in_category_tree.yview)
        self.fonts_in_category_tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky='ns')

        # Grid layout
        self.fonts_in_category_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Context menu
        self.setup_category_fonts_context_menu()

        # Bind events
        self.bind_category_fonts_events()
        
        
        
    def setup_scrollbars_FFT(self, parent, treeview, show_horizontal=False):
        """Set up scrollbars for a treeview."""
        vsb = ttk.Scrollbar(parent, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=vsb.set)
        
        if show_horizontal:
            hsb = ttk.Scrollbar(parent, orient="horizontal", command=treeview.xview)
            treeview.configure(xscrollcommand=hsb.set)
            hsb.grid(row=2, column=0, sticky='ew')
            
        vsb.grid(row=1, column=1, sticky='ns')

    def setup_category_style(self):
        """Configure styles for the categories treeview."""
        self.categories_treeview.tag_configure('bold', font=('TkDefaultFont', 13, 'bold'))
        self.categories_treeview.configure(style="LargeFont.Treeview")

    def setup_font_table_context_menu(self):
        """Set up context menu for font table."""
        self.context_menu_font_table = tk.Menu(self.font_table_tree, tearoff=0)
        self.context_menu_font_table.add_command(
            label="Copy Font Name", 
            command=self.event_manager.copy_font_name
        )
        self.context_menu_font_table.add_command(
            label="Copy Font Path", 
            command=self.event_manager.copy_font_path
        )

    def setup_category_fonts_context_menu(self):
        """Set up context menu for fonts in category."""
        self.context_menu_category = tk.Menu(self.fonts_in_category_tree, tearoff=0)
        self.context_menu_category.add_command(
            label="Copy Font Name",
            command=self.event_manager.copy_font_name_category
        )
        self.context_menu_category.add_command(
            label="Copy Font Path",
            command=self.event_manager.copy_font_path_category
        )

    def show_icon_selection_menu(self, event):
        """Handle right-click on category icon column."""
        item = self.categories_treeview.identify_row(event.y)
        if not item:
            return
        
        # Check if click was in icon column
        region = self.categories_treeview.identify_region(event.x, event.y)
        column = self.categories_treeview.identify_column(event.x)
        
        if region == "tree" or column == "#0":  # Icon column
            self.categories_treeview.selection_set(item)
            self.select_category_icon(item)



    def populate_fonts_in_category(self, category_label):
        """Populate the fonts in category treeview."""
        try:
            self.clear_fonts_in_category()

            category = self.font_manager.categories.get(category_label)
            if not category:
                return

            font_paths = category.fonts_list
            fonts_in_category = [f for f in self.font_manager.fonts if f.font_path in font_paths]

            for font in fonts_in_category:
                exists = any(f.font_path == font.font_path for f in self.font_manager.fonts)
                found_it = "Yes" if exists else "No"
                
                # Combine font name and style for display
                font_name_style = f"{font.font_name} - {font.font_style}" if exists else font.font_file

                item_id = self.fonts_in_category_tree.insert(
                    '', 'end',
                    values=(font_name_style, found_it, font.font_file)  # Update column order
                )
                
                self.fonts_in_category_mapping[item_id] = font if exists else None

        except Exception as e:
            logger.error(f"Error populating fonts in category: {str(e)}")
            messagebox.showerror("Error", f"Failed to populate fonts in category: {str(e)}")
            

    def get_selected_fonts(self):
        """Get selected FontInfo objects from the font table tree."""
        try:
            selected = self.font_table_tree.selection()
            fonts = []
            for item in selected:
                values = self.font_table_tree.item(item, 'values')
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
            selected = self.categories_treeview.selection()
            if not selected:
                return None
            return self.categories_treeview.item(selected[0], 'values')[2]
        except Exception as e:
            logger.error(f"Error getting selected category: {str(e)}")
            return None

    def get_category_item_by_id(self, category_id):
        """Find and return the treeview item ID for a given category ID."""
        try:
            for item in self.categories_treeview.get_children():
                values = self.categories_treeview.item(item, 'values')
                if str(values[3]) == str(category_id):
                    return item
            return None
        except Exception as e:
            logger.error(f"Error finding category by ID: {str(e)}")
            return None

    def bind_font_table_events(self):
        """Bind events for the font table treeview."""
        self.font_table_tree.bind("<Button-3>", self.show_font_table_context_menu)
        self.font_table_tree.bind("<Button-1>", self.hide_font_table_context_menu)
        self.font_table_tree.bind('<<TreeviewSelect>>', self.on_font_select)
        self.font_table_tree.bind('<Double-1>', self.on_double_click_font_table)
        self.font_table_tree.bind("<FocusIn>", 
            lambda e: self.style_manager.on_treeview_focus_in(self.font_table_tree))
        self.font_table_tree.bind("<FocusOut>", 
            lambda e: self.style_manager.on_treeview_focus_out(self.font_table_tree))

    def bind_category_events(self):
        """Bind events for the categories treeview."""
        self.categories_treeview.bind('<<TreeviewSelect>>', self.on_category_select)
        self.categories_treeview.bind("<FocusIn>", 
            lambda e: self.style_manager.on_treeview_focus_in(self.categories_treeview))
        self.categories_treeview.bind("<FocusOut>", 
            lambda e: self.style_manager.on_treeview_focus_out(self.categories_treeview))

    def bind_category_fonts_events(self):
        """Bind events for the fonts in category treeview."""
        self.fonts_in_category_tree.bind("<Button-3>", self.show_category_context_menu)
        self.fonts_in_category_tree.bind("<Button-1>", self.hide_category_context_menu)
        self.fonts_in_category_tree.bind('<<TreeviewSelect>>', self.on_fonts_in_category_select)
        self.fonts_in_category_tree.bind('<Double-1>', self.on_fonts_in_category_double_click)
        self.fonts_in_category_tree.bind("<FocusIn>", 
            lambda e: self.style_manager.on_treeview_focus_in(self.fonts_in_category_tree))
        self.fonts_in_category_tree.bind("<FocusOut>", 
            lambda e: self.style_manager.on_treeview_focus_out(self.fonts_in_category_tree))

    # Event Handlers
    def on_font_select(self, event):
        """Handle font selection in the font table."""
        try:
            selected_fonts = self.get_selected_fonts()
            if selected_fonts:
                font_info = selected_fonts[0]
                font_size = self.gui.font_table_render_frame.font_size
                display_text = f"{font_info.font_name} -- {font_info.font_style} -- Size: {font_size}"
                self.gui.font_table_render_frame.current_font_label.config(text=display_text)
                self.gui.font_table_render_frame.font_path = font_info.font_path
                self.gui.font_table_render_frame.render_text_on_canvas()
            else:
                font_size = self.gui.font_table_render_frame.font_size
                self.gui.font_table_render_frame.current_font_label.config(text=f"-- -- -- Size: {font_size}")
        except Exception as e:
            logger.error(f"Error handling font selection: {str(e)}")

    def on_category_select(self, event):
        """Handle category selection."""
        try:
            category_label = self.get_selected_category()
            if category_label:
                self.populate_fonts_in_category(category_label)
        except Exception as e:
            logger.error(f"Error handling category selection: {str(e)}")


    def on_fonts_in_category_select(self, event):
        """Handle font selection in the category view."""
        try:
            selected_items = self.fonts_in_category_tree.selection()
            if not selected_items:
                font_size = self.gui.font_table_render_frame.font_size
                self.gui.font_table_render_frame.current_font_label.config(text=f"-- -- -- Size: {font_size}")
                return

            selected_item = selected_items[0]
            font_info = self.fonts_in_category_mapping.get(selected_item)
            font_size = self.gui.font_table_render_frame.font_size

            if font_info:
                display_text = f"{font_info.font_name} -- {font_info.font_style} -- Size: {font_size}"
                self.gui.font_table_render_frame.current_font_label.config(text=display_text)
                self.gui.font_table_render_frame.font_path = font_info.font_path
                self.gui.font_table_render_frame.render_text_on_canvas()
            else:
                # Get filename from the third column now
                font_file = self.fonts_in_category_tree.item(selected_item, 'values')[2]
                display_text = f"{font_file} -- Missing -- Size: {font_size}"
                self.gui.font_table_render_frame.current_font_label.config(text=display_text)
        except Exception as e:
            logger.error(f"Error handling category font selection: {str(e)}")


    def on_fonts_in_category_double_click(self, event):
        """Handle double-click in the category fonts view."""
        try:
            selected_item = self.fonts_in_category_tree.focus()
            if selected_item:
                font_info = self.fonts_in_category_mapping.get(selected_item)
                if font_info:
                    messagebox.showinfo("Font Info",
                                    f"Font Name: {font_info.font_name}\n"
                                    f"Font Path: {font_info.font_path}")
                else:
                    # Get filename from the third column now
                    font_file = self.fonts_in_category_tree.item(selected_item, 'values')[2]
                    messagebox.showwarning("Font Missing",
                                       f"The font file '{font_file}' is missing.")
        except Exception as e:
            logger.error(f"Error handling category font double-click: {str(e)}")

    def on_double_click_font_table(self, event):
        """Handle double-click in the font table."""
        try:
            if event is None:
                return

            region = self.font_table_tree.identify("region", event.x, event.y)
            if region != "cell":
                return

            column = self.font_table_tree.identify_column(event.x)
            column_index = int(column.replace("#", "")) - 1
            column_id = self.font_table_tree["columns"][column_index]

            if column_id != "user_note":
                return

            row_id = self.font_table_tree.identify_row(event.y)
            if not row_id:
                return

            self.start_user_note_editing(row_id, column_id)
        except Exception as e:
            logger.error(f"Error handling font table double-click: {str(e)}")

    def start_user_note_editing(self, row_id, column_id):
        """Start editing a user note."""
        try:
            x, y, width, height = self.font_table_tree.bbox(row_id, column_id)
            value = self.font_table_tree.set(row_id, column_id)

            # Create Entry widget
            self.editing_entry = ttk.Entry(self.font_table_tree)
            self.editing_entry.place(x=x, y=y, width=width, height=height)
            self.editing_entry.insert(0, value)
            self.editing_entry.focus()

            # Bind events
            self.editing_entry.bind("<Return>", 
                lambda e: self.save_user_note(row_id, column_id))
            self.editing_entry.bind("<FocusOut>", 
                lambda e: self.cancel_edit())
        except Exception as e:
            logger.error(f"Error starting user note editing: {str(e)}")

    def save_user_note(self, row_id, column_id):
        """Save edited user note."""
        try:
            if hasattr(self, 'editing_entry'):
                new_value = self.editing_entry.get()
                self.font_table_tree.set(row_id, column_id, new_value)
                self.editing_entry.destroy()
                del self.editing_entry

                # Update FontInfo instance
                font_id = self.font_table_tree.set(row_id, "id")
                font_info = next((f for f in self.font_manager.fonts if f.id == font_id), None)
                if font_info:
                    font_info.user_note = new_value
                    logger.debug(f"Updated user_note for {font_info.font_name} to '{new_value}'")
                else:
                    logger.error(f"FontInfo with id {font_id} not found")
        except Exception as e:
            logger.error(f"Error saving user note: {str(e)}")

    def cancel_edit(self):
        """Cancel user note editing."""
        try:
            if hasattr(self, 'editing_entry'):
                self.editing_entry.destroy()
                del self.editing_entry
        except Exception as e:
            logger.error(f"Error canceling edit: {str(e)}")

    # Context Menu Handlers
    def show_font_table_context_menu(self, event):
        """Show context menu for font table."""
        try:
            selected = self.font_table_tree.identify_row(event.y)
            if selected:
                self.context_menu_font_table.post(event.x_root, event.y_root)
        except Exception as e:
            logger.error(f"Error showing font table context menu: {str(e)}")

    def hide_font_table_context_menu(self, event):
        """Hide the font table context menu."""
        try:
            self.context_menu_font_table.unpost()
        except Exception as e:
            logger.error(f"Error hiding font table context menu: {str(e)}")

    def show_category_context_menu(self, event):
        """Show context menu for fonts in category."""
        try:
            selected = self.fonts_in_category_tree.identify_row(event.y)
            if selected:
                self.context_menu_category.post(event.x_root, event.y_root)
        except Exception as e:
            logger.error(f"Error showing category context menu: {str(e)}")

    def hide_category_context_menu(self, event):
        """Hide the fonts in category context menu."""
        try:
            self.context_menu_category.unpost()
        except Exception as e:
            logger.error(f"Error hiding category context menu: {str(e)}")


    def select_matching_font_in_table(self, font_info):
        """Select a font in the font table matching the given FontInfo."""
        try:
            if not font_info:
                return False
                
            # Try to find matching font by font_file
            for item in self.font_table_tree.get_children():
                if self.font_table_tree.set(item, "font_file") == font_info.font_file:
                    self.font_table_tree.see(item)
                    self.font_table_tree.selection_set(item)
                    self.font_table_tree.focus(item)
                    return True
                    
            # If not found by font_file, try font_path as fallback
            for item in self.font_table_tree.get_children():
                if self.font_table_tree.set(item, "font_path") == font_info.font_path:
                    self.font_table_tree.see(item)
                    self.font_table_tree.selection_set(item)
                    self.font_table_tree.focus(item)
                    return True
                    
            return False
            
        except Exception as e:
            logger.error(f"Error selecting matching font: {str(e)}")
            return False
            
        
    def clear_fonts_in_category(self):
        """Clear all entries from the fonts in category tree."""
        try:
            self.fonts_in_category_tree.delete(*self.fonts_in_category_tree.get_children())
            self.fonts_in_category_mapping.clear()
            
            font_size = self.gui.font_table_render_frame.font_size
            self.gui.font_table_render_frame.current_font_label.config(
                text=f"-- -- -- Size: {font_size}")
                
            logger.debug("Cleared fonts in category view")
        except Exception as e:
            logger.error(f"Error clearing fonts in category: {str(e)}")

    def populate_font_table(self):
        """Populate the font table with all fonts."""
        try:
            self.font_table_tree.delete(*self.font_table_tree.get_children())
            
            for font in self.font_manager.fonts:
                self.font_table_tree.insert('', 'end', values=(
                    font.font_name,
                    font.font_style,
                    font.user_note,
                    font.license,
                    font.font_file,
                    font.font_path,
                    font.id
                ))
                
            logger.debug(f"Populated font table with {len(self.font_manager.fonts)} fonts")
            
        except Exception as e:
            logger.error(f"Error populating font table: {str(e)}")
            messagebox.showerror("Error", f"Failed to populate font table: {str(e)}")

    def save_state(self):
        """Save treeview state for the StateManager."""
        try:
            return {
                'selected_category': self.get_selected_category(),
                'font_table_selection': [
                    self.font_table_tree.item(item, 'values')[6]  # Save font IDs
                    for item in self.font_table_tree.selection()
                ]
            }
        except Exception as e:
            logger.error(f"Error saving treeview state: {str(e)}")
            return {}

    def load_state(self, state_data):
        """Load treeview state from the StateManager."""
        try:
            # Restore category selection
            category_label = state_data.get('selected_category')
            if category_label:
                for item in self.categories_treeview.get_children():
                    if self.categories_treeview.item(item, 'values')[2] == category_label:
                        self.categories_treeview.selection_set(item)
                        self.categories_treeview.see(item)
                        self.populate_fonts_in_category(category_label)
                        break

            # Restore font table selection
            font_ids = state_data.get('font_table_selection', [])
            if font_ids:
                for item in self.font_table_tree.get_children():
                    if self.font_table_tree.set(item, "id") in font_ids:
                        self.font_table_tree.selection_add(item)
            logger.debug("Treeview state loaded successfully")
        except Exception as e:
            logger.error(f"Error loading treeview state: {str(e)}")
            
            




    def load_default_icon(self):
        """Load the default category icon."""
        try:
            default_icon_path = os.path.join(os.path.dirname(__file__), 'cat_icon.png')
            if os.path.exists(default_icon_path):
                image = Image.open(default_icon_path)
                image = image.resize((32, 32), Image.Resampling.LANCZOS)
                self._default_icon = ImageTk.PhotoImage(image)
            else:
                logger.warning(f"Default category icon not found at {default_icon_path}")
                # Create empty icon if default not found
                image = Image.new('RGBA', (32, 32), (200, 200, 200, 128))
                self._default_icon = ImageTk.PhotoImage(image)
        except Exception as e:
            logger.error(f"Error loading default icon: {e}")
            image = Image.new('RGBA', (32, 32), (200, 200, 200, 128))
            self._default_icon = ImageTk.PhotoImage(image)

    def select_category_icon(self, item):
        """Show file dialog for selecting a category icon."""
        try:
            category_id = self.categories_treeview.item(item, 'values')[3]
            category_label = self.categories_treeview.item(item, 'values')[2]
            
            # Set default path for file dialog
            default_path = os.path.expanduser("~/.config/font_hyper/category_icons")
            os.makedirs(default_path, exist_ok=True)
            
            # Show file dialog
            file_types = [
                ('Image files', ('*.png', '*.jpg', '*.jpeg', '*.webp')),
                ('PNG files', '*.png'),
                ('JPEG files', '*.jpg;*.jpeg'),
                ('WebP files', '*.webp')
            ]
            
            file_path = filedialog.askopenfilename(
                title=f"Select an image file for icon - {category_label}",
                filetypes=file_types,
                initialdir=default_path
            )
            
            if file_path:
                # Get category and set icon
                category = next((cat for cat in self.font_manager.categories.values() 
                               if cat.idx == category_id), None)
                if category and category.set_icon_from_file(file_path):
                    # Update treeview with display icon
                    if hasattr(category, '_display_icon'):
                        self.categories_treeview.item(item, image=category._display_icon)
                    self.populate_categories()  # Refresh the entire treeview
                else:
                    messagebox.showerror("Error", "Failed to set category icon")
        
        except Exception as e:
            logger.error(f"Error selecting category icon: {e}")
            messagebox.showerror("Error", f"Failed to set category icon: {str(e)}")


    def populate_categories(self):
        """Populate the categories treeview."""
        try:
            self.categories_treeview.delete(*self.categories_treeview.get_children())
            
            for category_label, category in self.font_manager.categories.items():
                count = len(category.fonts_list)
                
                # Set installation status indicator
                inst = "@" if category.is_installed else ""
                category_id = category.idx
                
                # Set tags for bold font if installed
                tags = ('bold',) if category.is_installed else ()
                
                # Get category icon
                if hasattr(category, '_display_icon') and category._display_icon:
                    display_icon = category._display_icon
                else:
                    # Try to load icon if we have a file but no display icon
                    if category.category_icon_file:
                        category.load_category_icon()
                        display_icon = getattr(category, '_display_icon', self._default_icon)
                    else:
                        display_icon = self._default_icon
                
                # Insert with explicit tuple for values, icon, and tags for installed status
                self.categories_treeview.insert(
                    parent='',
                    index='end',
                    values=(str(count), inst, category_label, category_id),
                    tags=tags,
                    image=display_icon
                )
            
            logger.debug(f"Populated categories with {len(self.font_manager.categories)} categories")
            
        except Exception as e:
            logger.error(f"Error populating categories: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to populate categories: {str(e)}")
            

    def setup_categories_treeview(self):
        """Set up the categories treeview."""
        self.categories_treeview = ttk.Treeview(
            self.gui.categories_frame,
            columns=("Count", "Inst", "Label", "Id"),
            show='tree headings',
            selectmode='browse'
        )

        # Configure headings
        self.categories_treeview.heading("#0", text="Icon")
        self.categories_treeview.heading("Count", text="Count")
        self.categories_treeview.heading("Inst", text="Inst")
        self.categories_treeview.heading("Label", text="Label")
        self.categories_treeview.heading("Id", text="Id")

        # Configure columns
        # NOTE: column widths influence width of categories_treeview 
        self.categories_treeview.column("#0", width=58, anchor='w', stretch=False)  # Width for 32x32 icon
        self.categories_treeview.column("Count", width=30, anchor='center', stretch=False)
        self.categories_treeview.column("Inst", width=22, anchor='center', stretch=False)
        self.categories_treeview.column("Label", width=120, anchor='w', stretch=True)
        self.categories_treeview.column("Id", width=0, stretch=False)

        # Setup scrollbars
        vsb = ttk.Scrollbar(self.gui.categories_frame, orient="vertical", command=self.categories_treeview.yview)
        self.categories_treeview.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky='ns')

        # Grid layout
        self.categories_treeview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configure style
        self.setup_category_style()

        # Bind events
        self.bind_category_events()
        
        # Add right-click binding for icon selection
        self.categories_treeview.bind("<Button-3>", self.show_icon_selection_menu)
        
        
        


    def update_category_count(self, category_label):
        """Updates the font count for a specific category in the categories treeview."""
        try:
            # Find the category in the treeview
            category = self.font_manager.categories.get(category_label)
            if not category:
                logger.error(f"Category '{category_label}' not found")
                return

            # Count fonts in the category
            count = len(category.fonts_list)

            # Update the count in the treeview
            for item in self.categories_treeview.get_children():
                if self.categories_treeview.item(item, 'values')[2] == category_label:  # Label is in third column
                    current_values = list(self.categories_treeview.item(item, 'values'))
                    current_values[0] = str(count)  # Update count in first column
                    self.categories_treeview.item(item, values=tuple(current_values))
                    break

            logger.debug(f"Updated count for category '{category_label}' to {count}")

        except Exception as e:
            logger.error(f"Error updating category count: {str(e)}")
            traceback.print_exc()
            
            







        
