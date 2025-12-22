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
OUTPUT_IMAGE = os.path.join("images", "module7.png")
OUTPUT_MD = os.path.join("reports", "module7.md")

# Base Dimensions (At Scale 1.0)
BASE_WIDTH = 1600
BASE_HEIGHT = 1000
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

class Module7Complementaries:
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

    def render_plane(self, w, h, hue_a_deg, hue_b_deg):
        """
        Renders a 2D plane transitioning between two hues (X) and brightness (Y).
        """
        img = Image.new('RGB', (w, h))
        pixels = img.load()

        # Hue values in 0-1 range
        ha = hue_a_deg / 360.0
        hb = hue_b_deg / 360.0
        
        # Fixed saturation for the theoretical mix (medium-high to find matches)
        sat = 0.6 

        for y in range(h):
            # Y axis = Brightness (Value)
            val = 1.0 - (y / float(h))
            
            for x in range(w):
                # Distance from center (0.0 to 1.0)
                norm_x = (x / (w/2)) - 1.0
                
                if norm_x < 0:
                    current_hue = ha
                    current_sat = sat * abs(norm_x) # Fade sat towards center
                else:
                    current_hue = hb
                    current_sat = sat * abs(norm_x) # Fade sat towards center
                
                # Convert Theoretical Color to RGB
                r_th, g_th, b_th = colorsys.hsv_to_rgb(current_hue, current_sat, val)
                
                # Find closest match
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
        title_text = "MODULE 7: COMPLEMENTARY PLANES"
        id_text = "ID: NORD_MOD7_COMP"
        
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
        
        # Grid Configuration
        cols = 3
        rows = 2
        spacing_x = int(40 * scale)
        spacing_y = int(60 * scale)
        
        # Calculate plot size
        plot_w = (w - (2 * margin) - ((cols-1) * spacing_x)) // cols
        plot_h = (h - content_y - margin - ((rows-1) * spacing_y)) // rows

        pairs = [
            ("RED/CYAN", 0, 180, "ID:30"),
            ("ORANGE/AZURE", 30, 210, "ID:31"),
            ("YELLOW/BLUE", 60, 240, "ID:32"),
            ("CHARTREUSE/VIOLET", 90, 270, "ID:33"),
            ("GREEN/MAGENTA", 120, 300, "ID:34"),
            ("SPRING-GREEN/ROSE", 150, 330, "ID:35")
        ]

        for i, (label, ha, hb, id_str) in enumerate(pairs):
            r = i // cols
            c = i % cols
            
            x = margin + c * (plot_w + spacing_x)
            y = content_y + r * (plot_h + spacing_y)
            
            # Render and Paste Plot
            plot = self.render_plane(plot_w, plot_h, ha, hb)
            canvas.paste(plot, (x, y))
            self.draw_ui_element(draw, x, y, plot_w, plot_h, label, id_str, scale)

        return canvas

    def generate_markdown(self):
        md = f"""
# Module 7: Complementary Desaturation Planes
**Generated ID:** NORD_MOD7_COMP

This module visualizes how the palette handles transitions between opposing colors.

### The Visualization Logic
Each box represents a 2D slice of color space:
* **X-Axis (Hue/Saturation):** The left edge is Color A. The right edge is Color B (its opposite). The center is Neutral Gray.
* **Y-Axis (Brightness):** Top is White. Bottom is Black.

### Analysis
* **ID:30 (RED/CYAN):** Transition between Red and Cyan.
* **ID:31 (ORANGE/AZURE):** Transition between Orange and Azure.
* **ID:32 (YELLOW/BLUE):** Transition between Yellow and Blue.
* **ID:33 (CHARTREUSE/VIOLET):** Transition between Chartreuse and Violet.
* **ID:34 (GREEN/MAGENTA):** Transition between Green and Magenta.
* **ID:35 (SPRING-GREEN/ROSE):** Transition between Spring-Green and Rose.
"""
        with open(OUTPUT_MD, "w") as f:
            f.write(md)
        print(f"Markdown saved to {OUTPUT_MD}")

def run(scale=DEFAULT_SCALE):
    os.makedirs("images", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    study = Module7Complementaries()
    img = study.assemble(scale)
    img.save(OUTPUT_IMAGE)
    study.generate_markdown()
    print(f"Saved {OUTPUT_IMAGE}")
    print(f"MD Saved: {OUTPUT_MD}")

if __name__ == "__main__":
    run()
