# font_manager.py
# for license info (GPL3), see license.txt from font_hyper package

import os
import json
import logging
from .font_info import FontInfo
from .font_category import FontCategory

logger = logging.getLogger(__name__)

class FontManager:
    def __init__(self):
        self.font_paths_predefined = ['/usr/share/fonts/TTF']
        self.font_paths_user = []
        self.font_install_path = os.path.expanduser('~/.local/share/fonts/font_hyper/')
        self.fonts = []  # List of FontInfo objects
        self.categories = {}  # category_name: FontCategory instance
        self._font_paths_set = set()  # Helper set to track unique font paths
        self._font_filenames_dict = {}  # Helper dict to track filenames and their paths

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
        """Search for fonts in predefined and user-defined paths, handling duplicates."""
        # Reset the filename tracking dictionary
        self._font_filenames_dict = {}
        
        # Process system paths first
        self._process_font_paths(self.font_paths_predefined, is_system=True)
        
        # Then process user paths
        self._process_font_paths(self.font_paths_user, is_system=False)

    def _process_font_paths(self, paths, is_system=False):
        """Process font paths, handling duplicates based on filenames."""
        valid_paths, invalid_paths = self.verify_paths(paths)
        
        if invalid_paths:
            logger.warning(f"The following paths are invalid: {invalid_paths}")
            
        for path in valid_paths:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf')):
                        font_path = os.path.abspath(os.path.join(root, file))
                        
                        # Skip if this exact path is already loaded
                        if self.is_font_loaded(font_path):
                            continue
                            
                        # Convert filename to lowercase for comparison
                        file_lower = file.lower()
                        
                        # Check if we've seen this filename before (case-insensitive)
                        if file_lower in self._font_filenames_dict:
                            existing_path = self._font_filenames_dict[file_lower]
                            logger.info(f"Note: fontfile already in found fonts list (case-insensitive match), first font path: {existing_path}, second font path: {font_path}")
                            continue
                        
                        # If it's a new filename, process it
                        fi = FontInfo(font_path)
                        fi.extract_font_info()
                        fi.extract_license_info()
                        
                        if self.add_font(fi):
                            self._font_filenames_dict[file_lower] = font_path

    def to_dict(self):
        """Serialize FontManager to a dictionary, ensuring unique font paths."""
        unique_fonts = []
        seen_paths = set()
        for font in self.fonts:
            if font.font_path not in seen_paths:
                unique_fonts.append(font.to_dict())
                seen_paths.add(font.font_path)
            else:
                logger.debug(f"Duplicate font path skipped during serialization: {font.font_path}")

        return {
            'font_paths_predefined': self.font_paths_predefined,
            'font_paths_user': self.font_paths_user,
            'categories': {
                cat: self.categories[cat].to_dict()
                for cat in self.categories
            },
        }

    def from_dict(self, data):
        """Deserialize FontManager from a dictionary, ensuring unique font paths."""
        self.font_paths_predefined = data.get('font_paths_predefined', ['/usr/share/fonts/TTF'])
        self.font_paths_user = data.get('font_paths_user', [])
        
        # Reset the font paths set and fonts list
        self._font_paths_set = set()
        self.fonts = []
        self._font_filenames_dict = {}  # Reset filename tracking

        for f in data.get('fonts', []):
            font_path = os.path.abspath(os.path.expanduser(f.get('font_path', '')))
            if font_path and font_path not in self._font_paths_set:
                fi = FontInfo.from_dict(f)
                self.fonts.append(fi)
                self._font_paths_set.add(font_path)
                self._font_filenames_dict[os.path.basename(font_path).lower()] = font_path
            else:
                logger.debug(f"Duplicate or invalid font path skipped: {font_path}")

        # Handle categories
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
            logger.warning("'categories' has an unexpected format. Expected dict or list.")

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

    def remove_category(self, category_label):
        """Remove a category by its label."""
        if category_label in self.categories:
            del self.categories[category_label]
            return True
        return False

    def rename_category(self, old_label, new_label):
        """Rename a category."""
        if old_label in self.categories and new_label not in self.categories:
            category = self.categories.pop(old_label)
            category.label = new_label
            self.categories[new_label] = category
            return True
        return False

    def update_category_image(self, category_label, new_image_path):
        """Update the image path for a category."""
        if category_label in self.categories:
            self.categories[category_label].image_path = new_image_path
            return True
        return False

    def remove_font(self, font_path):
        """Remove a font from the manager."""
        font_info = self.get_font_info_by_path(font_path)
        if font_info:
            self.fonts.remove(font_info)
            self._font_paths_set.remove(font_path)
            filename = os.path.basename(font_path)
            if filename in self._font_filenames_dict:
                del self._font_filenames_dict[filename]
            
            # Remove from all categories
            for category in self.categories.values():
                if font_path in category.fonts_list:
                    category.fonts_list.remove(font_path)
            return True
        return False

    def get_fonts_in_category(self, category_label):
        """Get all FontInfo objects in a category."""
        if category_label not in self.categories:
            return []
        category = self.categories[category_label]
        return [self.get_font_info_by_path(path) for path in category.fonts_list if path in self._font_paths_set]

    def get_font_categories(self, font_path):
        """Get all categories that contain a specific font."""
        return [label for label, category in self.categories.items() 
                if font_path in category.fonts_list]

    def remove_font_from_category(self, category_label, font_path):
        """Remove a font from a specific category."""
        if category_label in self.categories:
            category = self.categories[category_label]
            if font_path in category.fonts_list:
                category.fonts_list.remove(font_path)
                self.update_category_info(category_label)
                return True
        return False

    def clear_category(self, category_label):
        """Remove all fonts from a category."""
        if category_label in self.categories:
            self.categories[category_label].fonts_list.clear()
            self.update_category_info(category_label)
            return True
        return False

    def get_duplicate_fonts(self):
        """Get a list of all duplicate fonts based on filename (case-insensitive)."""
        duplicates = {}
        for filename, path in self._font_filenames_dict.items():
            all_paths = [f.font_path for f in self.fonts 
                        if os.path.basename(f.font_path).lower() == filename]
            if len(all_paths) > 1:
                duplicates[filename] = all_paths
        return duplicates

    def save_to_file(self, filepath):
        """Save the font manager state to a JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error saving font manager state: {e}")
            return False

    def load_from_file(self, filepath):
        """Load the font manager state from a JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.from_dict(data)
            return True
        except Exception as e:
            logger.error(f"Error loading font manager state: {e}")
            return False
            
#

