# font_info.py

import os
import freetype
from uuid import uuid4


class FontInfo:
    def __init__(self, font_path):
        self.id = str(uuid4())  # Unique identifier
        self.font_path = os.path.abspath(os.path.expanduser(font_path))
        self.font_file = os.path.basename(self.font_path)
        self.font_name = self.get_font_name()
        self.font_family = self.get_font_family()
        self.font_style = self.get_font_style()
        self.font_styles = self.get_font_styles()
        self.user_note = ""      # New attribute for user notes
        self.license = ""        # New attribute for license information
        self.font_info = ""      # New attribute for font description

    def get_font_name(self):
        try:
            face = freetype.Face(self.font_path)
            return face.family_name.decode('utf-8') if face.family_name else "Unknown"
        except Exception:
            return "Unknown"

    def get_font_family(self):
        try:
            face = freetype.Face(self.font_path)
            return face.style_name.decode('utf-8') if face.style_name else "Regular"
        except Exception:
            return "Regular"

    def get_font_style(self):
        try:
            face = freetype.Face(self.font_path)
            return face.style_name.decode('utf-8') if face.style_name else "Regular"
        except Exception:
            return "Regular"

    def get_font_styles(self):
        # This can be expanded to retrieve actual styles if needed
        return ["Regular", "Bold", "Italic", "Bold Italic"]

    def extract_font_info(self):
        """Extracts font description from the font file."""
        try:
            # This is a placeholder. Actual implementation depends on the font file's metadata.
            # For example, using fontTools:
            from fontTools.ttLib import TTFont
            font = TTFont(self.font_path)
            name = ""
            for record in font['name'].names:
                if record.nameID == 4:  # Full font name
                    name = record.string.decode('utf-8', errors='ignore')
                    break
            self.font_info = name if name else "No description available."
        except Exception:
            self.font_info = "No description available."

    def extract_license_info(self):
        """Extracts license information from the font file."""
        try:
            # This is a placeholder. Actual implementation depends on the font file's metadata.
            # For example, using fontTools:
            from fontTools.ttLib import TTFont
            font = TTFont(self.font_path)
            license = ""
            for record in font['name'].names:
                if record.nameID == 13:  # License Description
                    license = record.string.decode('utf-8', errors='ignore')
                    break
            self.license = license if license else "No license information available."
        except Exception:
            self.license = "No license information available."

    def to_dict(self):
        return {
            'id': self.id,
            'font_name': self.font_name,
            'font_file': self.font_file,
            'font_family': self.font_family,
            'font_style': self.font_style,
            'font_styles': self.font_styles,
            'font_path': self.font_path,
            'user_note': self.user_note,
            'license': self.license,
            'font_info': self.font_info
        }

    @staticmethod
    def from_dict(data):
        fi = FontInfo(data['font_path'])
        fi.id = data.get('id', str(uuid4()))
        fi.font_name = data.get('font_name', fi.get_font_name())
        fi.font_file = data.get('font_file', fi.font_file)
        fi.font_family = data.get('font_family', fi.get_font_family())
        fi.font_style = data.get('font_style', fi.get_font_style())
        fi.font_styles = data.get('font_styles', fi.get_font_styles())
        fi.user_note = data.get('user_note', "")
        fi.license = data.get('license', "")
        fi.font_info = data.get('font_info', "")
        return fi
