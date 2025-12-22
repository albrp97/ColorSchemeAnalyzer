import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import math
import os
import urllib.request

# ==========================================
# CONFIGURATION
# ==========================================
DEFAULT_SCALE = 2.0
OUTPUT_IMAGE = os.path.join("images", "module8.png")
OUTPUT_MD = os.path.join("reports", "module8.md")

# Base Dimensions (At Scale 1.0)
BASE_WIDTH = 1600
BASE_HEIGHT = 1200
BASE_MARGIN = 40
BASE_SPACING = 20
# Nord Palette
PALETTE_HEX = [
    "#2E3440", "#3B4252", "#434C5E", "#4C566A", 
    "#D8DEE9", "#E5E9F0", "#ECEFF4",            
    "#8FBCBB", "#88C0D0", "#81A1C1", "#5E81AC", 
    "#BF616A", "#D08770", "#EBCB8B", "#A3BE8C", "#B48EAD" 
]

FONT_FILENAME = "JetBrainsMono-Regular.ttf"
FONT_URL = "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf"

def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

rgb_palette = [hex_to_rgb(c) for c in PALETTE_HEX]
palette_arr = np.array(rgb_palette)

def get_luminance(rgb): return 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
def get_saturation(rgb):
    r, g, b = [x/255.0 for x in rgb]
    _, s, _ = colorsys.rgb_to_hsv(r, g, b)
    return s

_sorted_by_lum = sorted(rgb_palette, key=get_luminance)
_sorted_by_sat = sorted(rgb_palette, key=get_saturation)

BG_COLOR = _sorted_by_lum[0]
TEXT_COLOR = _sorted_by_lum[-1]
UI_BORDER = _sorted_by_lum[min(3, len(_sorted_by_lum)-1)]
TEXT_DIM  = UI_BORDER
ACCENT    = _sorted_by_sat[-1]

class Module8PrimaryRanges:
    def __init__(self):
        pass

    def load_fonts(self, scale):
        if not os.path.exists(FONT_FILENAME):
            try: urllib.request.urlretrieve(FONT_URL, FONT_FILENAME)
            except: pass
        
        size_main = int(max(6, 14 * scale))
        size_header = int(max(10, 24 * scale))
        size_tiny = int(max(5, 10 * scale))
        
        try:
            self.font = ImageFont.truetype(FONT_FILENAME, size_main)
            self.font_header = ImageFont.truetype(FONT_FILENAME, size_header)
            self.font_tiny = ImageFont.truetype(FONT_FILENAME, size_tiny)
        except:
            self.font = ImageFont.load_default()
            self.font_header = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

    def draw_ui_element(self, draw, x, y, w, h, title, subtitle, scale):
        """
        Draws the component with text outside to prevent overlap.
        Title: Top Left (Above box)
        Subtitle: Bottom Right (Below box)
        """
        text_padding = int(5 * scale)
        
        # 1. Title (Top Left, Above Box)
        title_y = y - int(22 * scale) 
        draw.text((x, title_y), title, fill=TEXT_COLOR, font=self.font)
        
        # 2. Subtitle / ID (Bottom Right, Below Box)
        sub_bbox = draw.textbbox((0, 0), subtitle, font=self.font_tiny)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_y = y + h + text_padding
        
        # Draw subtitle aligned to right edge of the box
        draw.text((x + w - sub_w, sub_y), subtitle, fill=TEXT_DIM, font=self.font_tiny)
        
        # 3. Border (The Component Frame)
        draw.rectangle([x-1, y-1, x+w, y+h], outline=UI_BORDER, width=max(1, int(1*scale)))

    def get_closest_color_fast(self, r, g, b):
        target = np.array([r, g, b])
        dists = np.sum((palette_arr - target)**2, axis=1)
        return np.argmin(dists)

    def render_hue_strip(self, w, h, fixed_hue_deg):
        """
        Renders a strip where:
        X = Value (Brightness) 0 -> 1
        Y = Saturation 0 -> 1
        Hue = Fixed
        """
        img = Image.new('RGB', (w, h))
        pixels = img.load()
        
        hue = fixed_hue_deg / 360.0
        
        for y in range(h):
            # Y-Axis: Saturation
            # Top = 1.0 (Vivid), Bottom = 0.0 (Gray)
            sat = 1.0 - (y / float(h))
            
            for x in range(w):
                # X-Axis: Brightness (Value)
                # Left = 0.0 (Black), Right = 1.0 (White)
                val = x / float(w)
                
                # Get Theoretical Color
                r_th, g_th, b_th = colorsys.hsv_to_rgb(hue, sat, val)
                
                # Find Nearest Nord Color
                idx = self.get_closest_color_fast(int(r_th*255), int(g_th*255), int(b_th*255))
                pixels[x, y] = rgb_palette[idx]
        
        return img

    def assemble(self, scale=DEFAULT_SCALE):
        self.load_fonts(scale)
        w, h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
        margin, spacing = int(BASE_MARGIN * scale), int(BASE_SPACING * scale)
        canvas = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        # 1. Header
        title_text = "MODULE 8: PRIMARY RANGES"
        id_text = "ID: NORD_MOD8_RANGES"
        
        # Title (Top Left)
        draw.text((margin, margin), title_text, fill=TEXT_COLOR, font=self.font)
        
        # ID (Top Right)
        id_bbox = draw.textbbox((0, 0), id_text, font=self.font_tiny)
        id_w = id_bbox[2] - id_bbox[0]
        draw.text((w - margin - id_w, margin + int(5 * scale)), id_text, fill=TEXT_DIM, font=self.font_tiny)
        
        # Line
        line_y = margin + int(40 * scale)
        draw.line([(margin, line_y), (w - margin, line_y)], fill=UI_BORDER, width=max(1, int(1 * scale)))
        
        content_y = line_y + spacing + int(20 * scale)
        
        # Configuration for the 9 strips
        ranges = [
            ("RED RANGE", 0, "ID:36"),
            ("ORANGE RANGE", 30, "ID:37"),
            ("YELLOW RANGE", 60, "ID:38"),
            ("GREEN RANGE", 120, "ID:39"),
            ("CYAN RANGE", 180, "ID:40"),
            ("AZURE RANGE", 210, "ID:41"),
            ("BLUE RANGE", 240, "ID:42"),
            ("VIOLET RANGE", 270, "ID:43"),
            ("MAGENTA RANGE", 300, "ID:44")
        ]
        
        # Calculate height per strip
        strip_h = (h - content_y - margin - ((len(ranges)-1) * spacing)) // len(ranges)
        strip_w = w - (2 * margin)

        curr_y = content_y

        for label, hue, id_str in ranges:
            # 1. Render Strip
            strip = self.render_hue_strip(strip_w, strip_h, hue)
            canvas.paste(strip, (margin, curr_y))
            
            # 2. Draw UI Element
            self.draw_ui_element(draw, margin, curr_y, strip_w, strip_h, label, id_str, scale)
            
            curr_y += strip_h + spacing

        return canvas

    def generate_markdown(self):
        md = f"""
# Module 8: Primary Ranges
**Generated ID:** NORD_MOD8_RANGES

This module is a stress test for the palette across the 9 primary hue channels.

### The Logic
Each horizontal bar represents a specific hue (Red, Orange, Yellow, etc.).
* **Left to Right:** Darkness to Lightness (Value 0% -> 100%).
* **Bottom to Top:** Dullness to Vividness (Saturation 0% -> 100%).

### Analysis
* **ID:36 (RED RANGE):** Red hue channel.
* **ID:37 (ORANGE RANGE):** Orange hue channel.
* **ID:38 (YELLOW RANGE):** Yellow hue channel.
* **ID:39 (GREEN RANGE):** Green hue channel.
* **ID:40 (CYAN RANGE):** Cyan hue channel.
* **ID:41 (AZURE RANGE):** Azure hue channel.
* **ID:42 (BLUE RANGE):** Blue hue channel.
* **ID:43 (VIOLET RANGE):** Violet hue channel.
* **ID:44 (MAGENTA RANGE):** Magenta hue channel.
"""
        with open(OUTPUT_MD, "w") as f:
            f.write(md)
        print(f"Markdown saved to {OUTPUT_MD}")

def run(scale=DEFAULT_SCALE):
    os.makedirs("images", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    study = Module8PrimaryRanges()
    img = study.assemble(scale)
    img.save(OUTPUT_IMAGE)
    study.generate_markdown()
    print(f"Saved {OUTPUT_IMAGE}")
    print(f"MD Saved: {OUTPUT_MD}")

if __name__ == "__main__":
    run()
