

"""
script that downloads the emoji charset as a .woff2 font file and includes a function to iterate through available fonts to check which support the emoji charset range.


Features
    EMOJI_RANGES: Defines the Unicode ranges for emojis.
    fetch_fonts: Retrieves available fonts using the Google Fonts API.
    fonts_supporting_emoji: Filters fonts that support the emoji charset.
    download_font_woff2: Downloads a subsetted font in .woff2 format.


"""

import requests
import os

# Unicode ranges for emojis
EMOJI_RANGES = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Symbols
    (0x1F680, 0x1F6FF),  # Transport and map symbols
    (0x1F900, 0x1F9FF)   # Miscellaneous symbols and pictographs
]

# Google Fonts API URL and environment variable for API key
GOOGLE_FONTS_API_URL = "https://www.googleapis.com/webfonts/v1/webfonts"
API_KEY = os.getenv("GOOGLE_FONTS_API_KEY")


def unicode_to_range_string(ranges):
    """Convert Unicode ranges to a string format for font APIs."""
    return ",".join(f"U+{start:X}-{end:X}" for start, end in ranges)


def fetch_fonts(api_key):
    """Fetch available fonts using Google Fonts API."""
    response = requests.get(f"{GOOGLE_FONTS_API_URL}?key={api_key}")
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error fetching fonts: {response.status_code}")
        return []


def fonts_supporting_emoji(api_key, emoji_ranges):
    """Find fonts that support the specified emoji ranges."""
    fonts = fetch_fonts(api_key)
    supporting_fonts = []
    for font in fonts:
        subsets = font.get("subsets", [])
        if "emoji" in subsets:
            supporting_fonts.append(font["family"])
    return supporting_fonts


def download_font_woff2(font_name, ranges, output_dir="fonts"):
    """Download the subsetted font as a .woff2 file."""
    os.makedirs(output_dir, exist_ok=True)
    unicode_range = unicode_to_range_string(ranges)
    url = f"https://fonts.googleapis.com/css2?family={font_name}&text=&display=swap&subset=emoji"
    response = requests.get(url)

    if response.status_code == 200:
        # Extract .woff2 link from the CSS response
        css = response.text
        woff2_url = None
        for line in css.splitlines():
            if "woff2" in line:
                woff2_url = line.split("url(")[1].split(")")[0].strip("'")
                break

        if woff2_url:
            font_response = requests.get(woff2_url)
            if font_response.status_code == 200:
                font_path = os.path.join(output_dir, f"{font_name.replace(' ', '_')}.woff2")
                with open(font_path, "wb") as f:
                    f.write(font_response.content)
                print(f"Font downloaded: {font_path}")
            else:
                print(f"Error downloading font file: {font_response.status_code}")
        else:
            print("Could not find .woff2 URL in the CSS response.")
    else:
        print(f"Error fetching font CSS: {response.status_code}")


if __name__ == "__main__":
    if not API_KEY:
        print("Error: Google Fonts API key not set in environment variables.")
    else:
        # Find fonts supporting emojis
        emoji_fonts = fonts_supporting_emoji(API_KEY, EMOJI_RANGES)
        print(f"Fonts supporting emojis: {emoji_fonts}")

        # Download the first font that supports emojis
        if emoji_fonts:
            download_font_woff2(emoji_fonts[0], EMOJI_RANGES)


