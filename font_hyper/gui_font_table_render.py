# gui_font_table_render.py
# for license info (GPL3), see license.txt from font_hyper package

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import logging
import os
import traceback
import freetype
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageColor

logger = logging.getLogger(__name__)

class FontTableRenderFrame(ttk.LabelFrame):
    """
    Frame for rendering font previews and managing rendering options.
    Integrates with EventManager and StateManager.
    """
    def __init__(self, parent, font_manager, main_window):
        super().__init__(parent, text="RF", padding=1)
        self.font_manager = font_manager
        self.main_window = main_window
        self.event_manager = main_window.event_manager
        self.state_manager = main_window.state_manager
        
        # Initialize rendering attributes
        self.setup_rendering_attributes()
        
        # Initialize UI
        self.setup_ui()

    def setup_rendering_attributes(self):
        """Initialize all rendering-related attributes."""
        self.selected_fonts = []
        self.selected_category = None
        self.render_text = "Ägypter tragèn Avokado (zum Lîft)! @ $ € ¥ % »«→↓↑←^*#"
        self.font_color = "#000000"
        self.use_lcd_rendering = False
        self.use_auto_hinting = True
        self.use_kerning = True
        self.font_size = 36
        self.font_path = '/usr/share/fonts/TTF/DejaVuSans.ttf'
        self.photo = None
        self.logging_enabled = tk.BooleanVar(value=False)
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the render frame."""
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            logger.propagate = False

    def setup_ui(self):
        """Set up the user interface components."""
        self.setup_render_options_frame()
        self.setup_canvas()
        self.setup_size_controls()

    def setup_render_options_frame(self):
        """Set up the render options frame with all controls."""
        rof_frame = ttk.LabelFrame(self, text="Render Options Frame (ROF)", padding=2)
        rof_frame.pack(padx=2, pady=2, fill=tk.X)

        # Configure grid columns
        for i in range(5):
            weight = 1 if i == 1 else 0
            rof_frame.columnconfigure(i, weight=weight)

        # Render Text Entry
        self.setup_render_text_entry(rof_frame)
        
        # Control Buttons
        self.setup_control_buttons(rof_frame)
        
        # Rendering Options
        self.setup_rendering_options(rof_frame)
        
        # Current Font Label
        self.setup_current_font_label(rof_frame)
        

    def setup_render_text_entry(self, parent):
        """Set up the render text entry field."""
        from .utils import focus_next  # Import the focus_next function
        
        style = ttk.Style()
        style.configure("CurrentFont.TLabel", padding=(4, 4))  #font=("Helvetica", 18))
        lab = ttk.Label(parent, text="Render Text:", style="CurrentFont.TLabel")
        lab.grid(row=0, column=0, sticky="w", padx=4, pady=2)
        
        self.render_entry = ttk.Entry(parent, width=50)
        self.render_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.render_entry.insert(0, self.render_text)
        self.render_entry.bind("<Return>", focus_next)  # Add focus_next binding
        self.render_entry.bind("<KeyRelease>", lambda e: self.render_text_on_canvas())

        
    def setup_control_buttons(self, parent):
        """Set up control buttons."""
        self.color_button = ttk.Button(parent, text="Select Color", command=self.select_color)
        self.color_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        initial_text = "Hide Paths" if self.main_window.top_row_visible else "Show Paths"
        self.toggle_top_row_button = ttk.Button(parent, text=initial_text, 
                                              command=self.main_window.toggle_top_row)
        self.toggle_top_row_button.grid(row=0, column=3, sticky="e", padx=5, pady=5)

    def setup_rendering_options(self, parent):
        """Set up rendering option checkboxes."""
        options_frame = ttk.Frame(parent)
        options_frame.grid(row=1, column=0, columnspan=5, sticky="ew", padx=5, pady=5)
        
        for i in range(4):
            options_frame.columnconfigure(i, weight=1)

        # LCD Rendering
        self.lcd_var = tk.BooleanVar(value=self.use_lcd_rendering)
        self.lcd_check = ttk.Checkbutton(
            options_frame,
            text="LCD Rendering",
            variable=self.lcd_var,
            command=lambda: self.toggle_option('lcd')
        )
        self.lcd_check.grid(row=0, column=0, sticky="w", padx=5)

        # Auto Hinting
        self.auto_hint_var = tk.BooleanVar(value=self.use_auto_hinting)
        self.auto_hint_check = ttk.Checkbutton(
            options_frame,
            text="Auto Hinting",
            variable=self.auto_hint_var,
            command=lambda: self.toggle_option('hinting')
        )
        self.auto_hint_check.grid(row=0, column=1, sticky="w", padx=5)

        # Kerning
        self.kerning_var = tk.BooleanVar(value=self.use_kerning)
        self.kerning_check = ttk.Checkbutton(
            options_frame,
            text="Use Kerning",
            variable=self.kerning_var,
            command=lambda: self.toggle_option('kerning')
        )
        self.kerning_check.grid(row=0, column=2, sticky="w", padx=5)

        # Logging
        self.logging_check = ttk.Checkbutton(
            options_frame,
            text="Enable Logging",
            variable=self.logging_enabled,
            command=self.toggle_logging
        )
        self.logging_check.grid(row=0, column=3, sticky="w", padx=5)

    def setup_current_font_label(self, parent):
        """Set up the current font label."""
        self.current_font_label = ttk.Label(parent, 
                                          text=f"-- -- -- Size: {self.font_size}", 
                                          font=('TkDefaultFont', 16, 'bold'))
        self.current_font_label.grid(row=2, column=0, columnspan=5, 
                                   sticky="w", padx=10, pady=(0, 10))

    def setup_canvas(self):
        """Set up the rendering canvas."""
        self.canvas = tk.Canvas(self, bg="white", width=400, height=36)
        self.canvas.pack(padx=4, pady=4, fill=tk.BOTH, expand=True)

    def setup_size_controls(self):
        """Set up font size controls."""
        # Size slider
        self.size_slider = ttk.Scale(
            self,
            from_=6,
            to=92,
            orient=tk.HORIZONTAL,
            value=self.font_size,
            command=self.on_font_size_slider_value_changed
        )
        self.size_slider.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Size label
        self.size_label = ttk.Label(self, text=f"Font Size: {self.font_size}")
        self.size_label.pack(side=tk.LEFT, padx=10, pady=5)

    def toggle_logging(self):
        """Toggle logging on/off."""
        if self.logging_enabled.get():
            logger.setLevel(logging.INFO)
            logger.info("Logging has been enabled.")
        else:
            logger.setLevel(logging.WARNING)
            logger.info("Logging has been disabled.")

    def toggle_option(self, option):
        """Toggle rendering options and update preview."""
        if option == 'lcd':
            self.use_lcd_rendering = self.lcd_var.get()
        elif option == 'hinting':
            self.use_auto_hinting = self.auto_hint_var.get()
        elif option == 'kerning':
            self.use_kerning = self.kerning_var.get()
            logger.info(f"Kerning Enabled: {self.use_kerning}")
        self.render_text_on_canvas()

    def select_color(self):
        """Open color chooser dialog."""
        color = colorchooser.askcolor(initialcolor=self.font_color)[1]
        if color:
            self.font_color = color
            style_name = "Color.TButton"
            style = ttk.Style()
            style.configure(style_name, background=color)
            self.color_button.config(style=style_name)
            self.render_text_on_canvas()

    def focus_next_widget(self, event):
        """Move focus to next widget."""
        event.widget.tk_focusNext().focus()
        return "break"

    def on_font_size_slider_value_changed(self, value):
        """Handle font size slider changes."""
        try:
            self.font_size = int(float(value))
            self.size_label.config(text=f"Font Size: {self.font_size}")

            selected_fonts = self.main_window.treeview_manager.get_selected_fonts()
            if selected_fonts:
                font_info = selected_fonts[0]
                display_text = f"{font_info.font_name} -- {font_info.font_style} -- Size: {self.font_size}"
            elif self.font_path and os.path.isfile(self.font_path):
                try:
                    face = freetype.Face(self.font_path)
                    font_name = face.family_name.decode('utf-8') if face.family_name else "Unknown"
                    font_style = face.style_name.decode('utf-8') if face.style_name else "Regular"
                    display_text = f"{font_name} -- {font_style} -- Size: {self.font_size}"
                except:
                    display_text = f"-- -- -- Size: {self.font_size}"
            else:
                display_text = f"-- -- -- Size: {self.font_size}"

            self.current_font_label.config(text=display_text)
            self.render_text_on_canvas()
            
        except Exception as e:
            logger.exception("Error changing font size")
            messagebox.showerror("Font Size Error", f"Error changing font size: {str(e)}")

    def render_text_on_canvas(self):
        """Render text on the canvas using current settings."""
        text = self.render_entry.get()
        try:
            if not self.font_path or not os.path.isfile(self.font_path):
                raise FileNotFoundError(f"Font file not found: {self.font_path}")

            face = freetype.Face(self.font_path)
            load_flags = freetype.FT_LOAD_RENDER

            if self.use_lcd_rendering:
                load_flags |= freetype.FT_LOAD_TARGET_LCD

            if self.use_auto_hinting:
                load_flags |= freetype.FT_LOAD_FORCE_AUTOHINT

            face.set_char_size(self.font_size * 64)
            use_kerning_val = self.use_kerning and face.has_kerning

            # Calculate metrics
            face.load_char('X')
            ascent = face.size.ascender >> 6
            descent = face.size.descender >> 6
            height = ascent - descent

            # Calculate total width
            total_width = self.calculate_text_width(face, text, use_kerning_val)

            # Create image and render text
            image = self.create_text_image(face, text, total_width, height, 
                                         ascent, use_kerning_val, load_flags)

            # Update canvas
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(4, 4, image=self.photo, anchor="nw")

        except Exception as e:
            logger.exception("Error rendering text")
            messagebox.showerror("Render Error", f"Error rendering text: {str(e)}")

    def calculate_text_width(self, face, text, use_kerning):
        """Calculate total width needed for text."""
        total_width = 0
        previous_char = None

        for char in text:
            face.load_char(char)
            glyph_index = face.get_char_index(char)

            if use_kerning and previous_char is not None:
                kerning = face.get_kerning(previous_char, glyph_index)
                total_width += kerning.x >> 6

            total_width += face.glyph.advance.x >> 6
            previous_char = glyph_index

        return total_width

    def create_text_image(self, face, text, total_width, height, ascent, use_kerning, load_flags):
        """Create image and render text onto it."""
        margin = 4
        image = Image.new('RGBA', (total_width + margin * 2, height + margin * 2), 
                         (255, 255, 255, 0))
        pen_x = margin
        baseline_y = margin + ascent
        previous_char = None
        rgb_color = ImageColor.getrgb(self.font_color)

        for char in text:
            try:
                glyph_index = face.get_char_index(char)
                
                if use_kerning and previous_char is not None:
                    kerning = face.get_kerning(previous_char, glyph_index)
                    pen_x += kerning.x >> 6

                face.load_char(char, load_flags)
                bitmap = face.glyph.bitmap
                
                if bitmap.width > 0 and bitmap.rows > 0:
                    glyph_image = (self.process_subpixel_rendering(bitmap, rgb_color) 
                                 if self.use_lcd_rendering 
                                 else self.process_normal_rendering(bitmap, rgb_color))

                    x = pen_x + face.glyph.bitmap_left
                    y = baseline_y - face.glyph.bitmap_top
                    image.paste(glyph_image, (x, y), glyph_image)
                    logger.debug(f"Rendered character '{char}' at position ({x}, {y})")
                else:
                    logger.debug(f"Character '{char}' has no bitmap. Skipping rendering.")

                pen_x += face.glyph.advance.x >> 6
                previous_char = glyph_index

            except Exception as e:
                logger.exception(f"Error rendering character '{char}'")
                continue

        return image

    def process_normal_rendering(self, bitmap, rgb_color):
        """Process normal (non-LCD) rendering of a glyph."""
        try:
            buffer = bytes(bitmap.buffer)
            glyph_image = Image.frombytes('L', (bitmap.width, bitmap.rows), buffer)
            rgba_color = rgb_color + (255,)
            colored_glyph = Image.new('RGBA', glyph_image.size, rgba_color)
            colored_glyph.putalpha(glyph_image)
            return colored_glyph
        except Exception as e:
            logger.exception("Error in normal rendering")
            return Image.new('RGBA', (1, 1), (0, 0, 0, 0))

    def process_subpixel_rendering(self, bitmap, rgb_color):
        """Process LCD subpixel rendering of a glyph."""
        try:
            rows = bitmap.rows
            pitch = abs(bitmap.pitch)
            width = bitmap.width

            if width % 3 != 0:
                raise ValueError("Bitmap width must be multiple of 3 for LCD rendering")

            display_pixels = width // 3

            if pitch < width:
                raise ValueError("Invalid pitch for LCD rendering")

            # Convert bitmap buffer to numpy array
            buffer_array = np.frombuffer(bytes(bitmap.buffer), dtype=np.uint8)
            expected_size = rows * pitch
            
            if buffer_array.size < expected_size:
                raise ValueError(f"Buffer size {buffer_array.size} smaller than expected {expected_size}")

            # Reshape and process buffer
            buffer_array = buffer_array[:expected_size].reshape((rows, pitch))
            
            # Extract RGB channels
            r = buffer_array[:, :3 * display_pixels:3]
            g = buffer_array[:, 1:3 * display_pixels:3]
            b = buffer_array[:, 2:3 * display_pixels:3]

            # Apply text color
            text_r, text_g, text_b = rgb_color
            r = r.astype(np.uint16)
            g = g.astype(np.uint16)
            b = b.astype(np.uint16)

            glyph_r = np.clip((r * text_r) // 255, 0, 255).astype(np.uint8)
            glyph_g = np.clip((g * text_g) // 255, 0, 255).astype(np.uint8)
            glyph_b = np.clip((b * text_b) // 255, 0, 255).astype(np.uint8)

            # Create final image
            glyph_data = np.stack((glyph_r, glyph_g, glyph_b), axis=-1)
            alpha_data = np.maximum(np.maximum(r, g), b).clip(0, 255).astype(np.uint8)
            
            glyph_image = Image.fromarray(glyph_data, 'RGB').convert('RGBA')
            glyph_image.putalpha(Image.fromarray(alpha_data, 'L'))

            logger.debug(f"Processed subpixel rendering for glyph: {glyph_image.size}")
            return glyph_image

        except Exception as e:
            logger.exception("Error in subpixel rendering")
            return Image.new('RGBA', (1, 1), (0, 0, 0, 0))

    def update_current_font(self, font_info=None):
        """Update the current font display and rendering."""
        try:
            if font_info:
                self.font_path = font_info.font_path
                display_text = f"{font_info.font_name} -- {font_info.font_style} -- Size: {self.font_size}"
            else:
                display_text = f"-- -- -- Size: {self.font_size}"
            
            self.current_font_label.config(text=display_text)
            self.render_text_on_canvas()
            
        except Exception as e:
            logger.exception("Error updating current font")
            messagebox.showerror("Font Update Error", f"Error updating font: {str(e)}")

    def save_state(self):
        """Save render frame state for the StateManager."""
        return {
            'render_text': self.render_entry.get(),
            'font_color': self.font_color,
            'font_size': self.font_size,
            'use_lcd_rendering': self.use_lcd_rendering,
            'use_auto_hinting': self.use_auto_hinting,
            'use_kerning': self.use_kerning
        }

    def load_state(self, state_data):
        """Load render frame state from the StateManager."""
        try:
            self.render_entry.delete(0, tk.END)
            self.render_entry.insert(0, state_data.get('render_text', self.render_text))
            self.font_color = state_data.get('font_color', self.font_color)
            self.font_size = state_data.get('font_size', self.font_size)
            self.use_lcd_rendering = state_data.get('use_lcd_rendering', self.use_lcd_rendering)
            self.use_auto_hinting = state_data.get('use_auto_hinting', self.use_auto_hinting)
            self.use_kerning = state_data.get('use_kerning', self.use_kerning)

            # Update UI elements
            self.lcd_var.set(self.use_lcd_rendering)
            self.auto_hint_var.set(self.use_auto_hinting)
            self.kerning_var.set(self.use_kerning)
            self.size_slider.set(self.font_size)
            self.size_label.config(text=f"Font Size: {self.font_size}")

            # Update rendering
            self.render_text_on_canvas()
            
        except Exception as e:
            logger.exception("Error loading render frame state")
            messagebox.showerror("State Load Error", f"Error loading render frame state: {str(e)}")
            
