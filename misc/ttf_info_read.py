import freetype


file_path = '/usr/share/fonts/TTF/DejaVuSans.ttf'


def get_font_info(file_path):
    # Load the font face
    face = freetype.Face(file_path)
    
    # Access the 'name' table directly
    name_table = face.get_sfnt_name

    # Define a helper function to get name entries
    def get_name_entry(name_table, name_id):
        for i in range(face.sfnt_name_count):
            name_entry = name_table(i)
            if name_entry.name_id == name_id:
                return name_entry.string.decode('utf-8', errors='ignore')
        return "Not Available"

    # Define name IDs for the information we want to retrieve
    name_ids = {
        "Font Name": 1,
        "Font Family": 16,
        "Font Subfamily": 17,
        "Full Font Name": 4,
        "Version": 5,
        "PostScript Name": 6,
        "Trademark": 7,
        "Manufacturer": 8,
        "Designer": 9,
        "Description": 10,
        "Vendor URL": 11,
        "Designer URL": 12,
        "License Description": 13,
        "License Info URL": 14,
        "Preferred Family": 16,
        "Preferred Subfamily": 17,
        "Compatible Full": 18,
        "Sample Text": 19,
        "PostScript CID": 20,
        "WWS Family Name": 21,
        "WWS Subfamily Name": 22,
    }
    
    font_info = {name: get_name_entry(name_table, id) for name, id in name_ids.items()}
    
    # Extracting additional information
    additional_info = {
        "Number of Glyphs": face.num_glyphs,
        "Number of Faces": face.num_faces,
        "Units per EM": face.units_per_EM,
        "Ascender": face.ascender,
        "Descender": face.descender,
        "Height": face.height,
        "Max Advance Width": face.max_advance_width,
        "Max Advance Height": face.max_advance_height,
    }
    
    font_info.update(additional_info)

    # Print font information
    for key, value in font_info.items():
        print(f"{key}: {value}")

# Example usage
# file_path = "path/to/your/font.ttf"  # Replace with the path to your TTF or OTF file
get_font_info(file_path)
