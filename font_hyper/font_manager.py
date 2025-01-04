# font_manager.py
# for license info (GPL3), see license.txt from font_hyper package

import os
import json
from .font_info import FontInfo
from .font_category import FontCategory


class FontManager:
    def __init__(self):
        self.font_paths_predefined = ['/usr/share/fonts/TTF']
        self.font_paths_user = []
        self.font_install_path = os.path.expanduser('~/.local/share/fonts/font_hyper/')
        self.fonts = []  # List of FontInfo objects
        self.categories = {}  # category_name: FontCategory instance
        self._font_paths_set = set()  # Helper set to track unique font paths

    def verify_paths(self, paths):
        """Verify the existence of given paths."""
        valid = [os.path.abspath(os.path.expanduser(path)) for path in paths if os.path.exists(os.path.abspath(os.path.expanduser(path)))]
        invalid = [path for path in paths if os.path.abspath(os.path.expanduser(path)) not in valid]
        return valid, invalid

    def is_font_loaded(self, font_path):
        """Check if a font with the given path is already loaded."""
        return font_path in self._font_paths_set

    def add_font(self, font_info):
        """Add a FontInfo object if its path is unique."""
        if font_info.font_path not in self._font_paths_set:
            self.fonts.append(font_info)
            self._font_paths_set.add(font_info.font_path)
            return True
        return False

    def search_fonts(self):
        """Search for fonts in predefined and user-defined paths."""
        all_paths = self.font_paths_predefined + self.font_paths_user
        valid_paths, invalid_paths = self.verify_paths(all_paths)
        if invalid_paths:
            print(f"Warning: The following paths are invalid: {invalid_paths}")
        for path in valid_paths:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf')):
                        font_path = os.path.abspath(os.path.join(root, file))
                        if not self.is_font_loaded(font_path):
                            fi = FontInfo(font_path)
                            fi.extract_font_info()
                            fi.extract_license_info()
                            self.add_font(fi)

    def add_category(self, category_label, image_path=""):
        """Add a new category."""
        if category_label not in self.categories:
            self.categories[category_label] = FontCategory(label=category_label, image_path=image_path)

    def assign_fonts_to_category(self, category_label, fonts):
        """Assign fonts to a specified category."""
        if category_label in self.categories:
            for font in fonts:
                if font.font_path not in self.categories[category_label].fonts_list:
                    self.categories[category_label].fonts_list.append(font.font_path)
            # Update category info after assignment
            self.update_category_info(category_label)

    def to_dict(self):
        """Serialize FontManager to a dictionary, ensuring unique font paths."""
        unique_fonts = []
        seen_paths = set()
        for font in self.fonts:
            if font.font_path not in seen_paths:
                unique_fonts.append(font.to_dict())
                seen_paths.add(font.font_path)
            else:
                print(f"Duplicate font path skipped during serialization: {font.font_path}")

        return {
            'font_paths_predefined': self.font_paths_predefined,
            'font_paths_user': self.font_paths_user,
             #'font_install_path': self.font_install_path, # do not save install path
             #'fonts': unique_fonts, # set fonts saving to INACTIVE, disabled
            'categories': {
                cat: self.categories[cat].to_dict()
                for cat in self.categories
            },
        }

    def from_dict(self, data):
        """Deserialize FontManager from a dictionary, ensuring unique font paths."""
        self.font_paths_predefined = data.get('font_paths_predefined', ['/usr/share/fonts/TTF'])
        self.font_paths_user = data.get('font_paths_user', [])

        ## do not load install path, use path from config
        #self.font_install_path = os.path.expanduser(data.get('font_install_path', '~/.local/share/fonts/font_mang/'))
        
        # Reset the font paths set and fonts list
        self._font_paths_set = set()
        self.fonts = []

        for f in data.get('fonts', []):
            font_path = os.path.abspath(os.path.expanduser(f.get('font_path', '')))
            if font_path and font_path not in self._font_paths_set:
                fi = FontInfo.from_dict(f)
                self.fonts.append(fi)
                self._font_paths_set.add(font_path)
            else:
                print(f"Duplicate or invalid font path skipped: {font_path}")

        # Handle categories as before
        self.categories = {}
        categories_data = data.get('categories', {})

        if isinstance(categories_data, list):
            for cat_data in categories_data:
                category = FontCategory.from_dict(cat_data)
                self.categories[category.label] = category
        elif isinstance(categories_data, dict):
            for cat_label, cat_data in categories_data.items():
                category = FontCategory.from_dict(cat_data)
                self.categories[cat_label] = category
        else:
            print("Warning: 'categories' has an unexpected format. Expected dict or list.")

    def get_font_info_by_path(self, font_path):
        """Retrieve FontInfo object by its path."""
        for font in self.fonts:
            if font.font_path == font_path:
                return font
        return None

    def update_category_info(self, category_label):
        """Updates font_info and license for a specific category."""
        category = self.categories.get(category_label)
        if not category:
            return
        category.generate_font_info_and_license(self)
        category.generate_preview_image(self)
