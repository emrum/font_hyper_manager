# font_category.py

import json
import os
import time
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont, ImageTk
import logging
from io import BytesIO
import base64

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FontCategory:
    """
    Represents a category of fonts with associated metadata and preview capabilities.
    Manages category icons, preview images, and font lists.
    """
    def __init__(self, label, image_path="", fonts_list=None, font_info="", license_info=""):
        """
        Initialize a new FontCategory.
        
        Args:
            label (str): The display name of the category
            image_path (str): Optional path to a preview image
            fonts_list (list): Optional list of font paths
            font_info (str): Optional font description
            license_info (str): Optional license information
        """
        self.idx = str(uuid4())  # Unique identifier using UUID
        self.label = label
        self.image_path = os.path.abspath(os.path.expanduser(image_path)) if image_path else ""
        self.fonts_list = fonts_list if fonts_list is not None else []

        self._category_icon = None  # PhotoImage instance
        self.category_icon_file = ""  # Path to the icon file relative to category_icons directory
        self.user_note = ""  # Custom notes for the font, set by the user
        self.font_info = font_info  # Font description from font file
        self.license = license_info  # License info from font file
        self.preview_image = None  # Rendered preview image, Pillow Image
        self.preview_image_size = (0, 0)
        self.preview_font_size = 24  # The font size used for rendering the preview image
        self.is_installed = False  # Set to true if the font category was installed, or false if removed


    @property
    def category_icon(self):
        """Gets the category icon, loading it if necessary."""
        try:
            if self._category_icon is None and self.category_icon_file:
                self.load_category_icon()
            return self._category_icon
        except Exception as e:
            logger.error(f"Error getting category icon: {e}")
            return None
            

    def load_category_icon(self):
        """Loads the category icon from file."""
        try:
            if self.category_icon_file:
                config_dir = os.path.expanduser("~/.config/font_hyper")
                icon_path = os.path.join(config_dir, "category_icons", self.category_icon_file)
                if os.path.exists(icon_path):
                    # Load full size icon (64x64) for storage
                    image = Image.open(icon_path)
                    image = image.resize((64, 64), Image.Resampling.LANCZOS)
                    self._category_icon = ImageTk.PhotoImage(image)
                    
                    # Create display version (32x32)
                    display_image = image.resize((32, 32), Image.Resampling.LANCZOS)
                    self._display_icon = ImageTk.PhotoImage(display_image)
                else:
                    self._category_icon = None
                    self._display_icon = None
                    logger.warning(f"Icon file not found: {icon_path}")
        except Exception as e:
            logger.error(f"Error loading category icon: {e}")
            self._category_icon = None
            self._display_icon = None
            

    def generate_font_info_and_license(self, font_manager):
        """
        Aggregates font descriptions and license information from all fonts in the category.
        
        Args:
            font_manager: The FontManager instance to use for font lookups
        """
        descriptions = []
        licenses = set()
        for font_path in self.fonts_list:
            font_info = font_manager.get_font_info_by_path(font_path)
            if font_info:
                if font_info.font_info:
                    descriptions.append(font_info.font_info)
                if font_info.license:
                    licenses.add(font_info.license)
        self.font_info = "\n".join(descriptions) if descriptions else "Not available."
        self.license = "\n".join(licenses) if licenses else "Not available"

    def generate_preview_image(self, font_manager, sample_text="The quick brown fox"):
        """
        Generates a preview image using the first available font in the category.
        
        Args:
            font_manager: The FontManager instance to use for font lookups
            sample_text (str): The text to render in the preview image
        """
        if not self.fonts_list:
            self.preview_image = None
            return

        font_info = font_manager.get_font_info_by_path(self.fonts_list[0])
        if not font_info:
            self.preview_image = None
            return

        try:
            font = ImageFont.truetype(font_info.font_path, self.preview_font_size)
            # Create a temporary image to calculate text size
            temp_image = Image.new('RGB', (1, 1))
            draw = ImageDraw.Draw(temp_image)
            bbox = draw.textbbox((0, 0), sample_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Add padding
            padding = 20
            image = Image.new('RGB', (text_width + padding, text_height + padding), color='white')
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), sample_text, font=font, fill='black')
            self.preview_image = image
            self.preview_image_size = image.size
        except Exception as e:
            logger.error(f"Error generating preview image: {e}")
            self.preview_image = None

    def to_dict(self):
        """
        Converts the category to a dictionary for serialization.
        
        Returns:
            dict: The category data as a dictionary
        """
        data = {
            'idx': self.idx,
            'label': self.label,
            'image_path': self.image_path,
            'fonts_list': self.fonts_list,
            'user_note': self.user_note,
            'font_info': self.font_info,
            'license': self.license,
            'is_installed': self.is_installed,
            'category_icon_file': self.category_icon_file  # Save only the filename
        }
        if 0  and self.preview_image: # if 0, disable preview save 
            buffered = BytesIO()
            self.preview_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            data['preview_image'] = img_str
            data['preview_image_size'] = self.preview_image_size
            data['preview_font_size'] = self.preview_font_size
        else:
            data['preview_image'] = None
            data['preview_image_size'] = self.preview_image_size
            data['preview_font_size'] = self.preview_font_size
        return data

    @staticmethod
    def from_dict(data):
        """
        Creates a new FontCategory instance from a dictionary.
        
        Args:
            data (dict): The dictionary containing category data
            
        Returns:
            FontCategory: A new FontCategory instance
        """
        label = data.get('label', 'Unnamed Category')
        image_path = data.get('image_path', "")
        fonts_list = data.get('fonts_list', [])
        font_info = data.get('font_info', "")
        license_info = data.get('license', "")
        category = FontCategory(label, image_path, fonts_list, font_info, license_info)
        category.idx = data.get('idx', str(uuid4()))
        category.user_note = data.get('user_note', "")
        category.is_installed = data.get('is_installed', False)
        category.category_icon_file = data.get('category_icon_file', "")  # Load the filename

        # Handle preview_image deserialization
        preview_image_str = data.get('preview_image')
        if preview_image_str:
            try:
                img_data = base64.b64decode(preview_image_str)
                image = Image.open(BytesIO(img_data))
                category.preview_image = image
                category.preview_image_size = tuple(data.get('preview_image_size', (0, 0)))
                category.preview_font_size = data.get('preview_font_size', 24)
            except Exception as e:
                logger.error(f"Error loading preview image: {e}")
                category.preview_image = None
        else:
            category.preview_image = None
            category.preview_image_size = tuple(data.get('preview_image_size', (0, 0)))
            category.preview_font_size = data.get('preview_font_size', 24)

        return category
        







    def set_icon_from_file(self, file_path):
        """
        Sets a new icon from the given file path.
        If file is already in the icons directory, uses it directly.
        Otherwise, copies the file to the category_icons directory.
        
        Args:
            file_path (str): Path to the image file to use as icon
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not file_path or not os.path.exists(file_path):
                return False

            # Get paths
            config_dir = os.path.expanduser("~/.config/font_hyper")
            icons_dir = os.path.join(config_dir, "category_icons")
            os.makedirs(icons_dir, exist_ok=True)

            # Check if file is already in icons directory
            is_in_icons_dir = os.path.dirname(os.path.abspath(file_path)) == os.path.abspath(icons_dir)
            
            # Set filename
            if is_in_icons_dir:
                new_filename = os.path.basename(file_path)
                new_path = file_path
            else:
                # Create new filename and path for copied file
                ext = os.path.splitext(file_path)[1].lower()
                new_filename = f"cat_icon_{self.idx}{ext}"
                new_path = os.path.join(icons_dir, new_filename)

            # Load and resize image
            image = Image.open(file_path)
            image = image.convert('RGBA')  # Ensure alpha channel support
            
            # Create storage version (64x64)
            if max(image.size) > 64:
                image.thumbnail((64, 64), Image.Resampling.LANCZOS)
            else:
                image = image.resize((64, 64), Image.Resampling.LANCZOS)
                
            # Create display version (32x32)
            display_image = image.resize((32, 32), Image.Resampling.LANCZOS)

            # Save file only if it's not already in the icons directory
            if not is_in_icons_dir:
                image.save(new_path, format='PNG')  # Always save as PNG for consistency
            
            # Update category icons
            self.category_icon_file = new_filename
            self._category_icon = ImageTk.PhotoImage(image)
            self._display_icon = ImageTk.PhotoImage(display_image)
            
            return True
        except Exception as e:
            logger.error(f"Error setting category icon: {e}")
            return False
