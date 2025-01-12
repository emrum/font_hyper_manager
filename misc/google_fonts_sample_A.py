import os
import requests


"""
# linux: export GOOGLE_FONTS_API_KEY="your_api_key_here" 
# default charset:  ISO 8859-1 (Latin-1)


charsets:
Windows-1252:
    A Microsoft extension of ISO 8859-1.
    Adds the Euro sign (€) and other characters.

UTF-8:
    A universal character encoding for Unicode.
    Fully supports the Euro sign (€) and many more symbols from all languages.
    


1. Subset for Emoticons and Smileys

Emojis and smileys are in specific Unicode ranges:

    Basic Emoticons: U+1F600 to U+1F64F
    Supplemental Symbols and Pictographs: U+1F300 to U+1F5FF
    Transport and Map Symbols: U+1F680 to U+1F6FF
    Miscellaneous Symbols and Pictographs: U+1F900 to U+1F9FF
    Additional Emojis: Various ranges, like U+2600 to U+26FF (e.g., ☀, ☂).
    
The Euro sign (€) is located at U+20AC. If this is your only requirement, your subset is limited to just one character.



Use Tools Like pyftsubset (From FontTools)
This tool allows you to subset existing font files based on Unicode ranges.
Example to subset emojis and the Euro sign:
pyftsubset input.ttf --output-file=output.ttf --unicodes=U+20AC,U+1F600-1F64F,U+1F300-1F5FF



# Unicode ranges for emojis and Euro sign
ranges = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Symbols
    (0x20AC, 0x20AC)     # Euro sign
]

# Generate relevant characters
subset = []
for start, end in ranges:
    subset.extend(chr(code) for code in range(start, end + 1))

# Print or use the subset
print("Subset characters:", subset)




 Use Tools Like pyftsubset (From FontTools)
This tool allows you to subset existing font files based on Unicode ranges.
Example to subset emojis and the Euro sign:
pyftsubset input.ttf --output-file=output.ttf --unicodes=U+20AC,U+1F600-1F64F,U+1F300-1F5FF



web request for subset
https://fonts.googleapis.com/css2?family=Noto+Color+Emoji&subset=emoji


Storage Optimization
    Compress the subset font file (e.g., .woff2).
    Use only the subsetted characters during rendering (e.g., define custom @font-face in CSS).



Categories include:

    sans-serif
    serif
    display
    handwriting
    monospace


You can sort fonts by popularity, trending, or date using the API.
response = requests.get(f"{API_URL}?key={api_key}&sort=popularity")


You can extract these categories dynamically by iterating through the API's response data:
categories = set(font.get("category") for font in fonts)

"""

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_FONTS_API_KEY")
API_URL = "https://www.googleapis.com/webfonts/v1/webfonts"

def fetch_fonts_by_category(api_key):
    if not api_key:
        print("Error: API key not found in environment variables.")
        return {}
    response = requests.get(f"{API_URL}?key={api_key}")
    if response.status_code == 200:
        fonts = response.json().get("items", [])
        categories = {}
        for font in fonts:
            category = font.get("category")
            font_name = font.get("family")
            if category not in categories:
                categories[category] = []
            categories[category].append(font_name)
        return categories
    else:
        print(f"Error fetching fonts: {response.status_code}")
        return {}


if __name__ == "__main__":
    categories = fetch_fonts_by_category(API_KEY)
    if categories:
        for category, fonts in categories.items():
            print(f"Category: {category} ({len(fonts)} fonts)")
            for font in fonts:
                print(f"  - {font}")


