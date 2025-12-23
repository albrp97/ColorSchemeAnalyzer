import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import os
import random

# ==========================================
# CONFIGURATION
# ==========================================
DEFAULT_SCALE = 2.0
OUTPUT_IMAGE = os.path.join("images", "module4.png")
OUTPUT_MD = os.path.join("reports", "module4.md")

# Base Dimensions (At Scale 1.0)
BASE_WIDTH = 1600
BASE_HEIGHT = 700
BASE_MARGIN = 40
BASE_SPACING = 20

# Configuration inherited from main.py
PALETTE_HEX = []
BG_COLOR = (0, 0, 0)
UI_BORDER = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
TEXT_DIM = (0, 0, 0)
ACCENT = (0, 0, 0)
FONT_FILENAME = ""
FONT_URL = ""

# Derived
rgb_palette = []
luma_sorted_colors = []
hue_sorted_colors = []

def run(scale=DEFAULT_SCALE, color_scheme=None):
    if color_scheme:
        global PALETTE_HEX, BG_COLOR, UI_BORDER, TEXT_COLOR, TEXT_DIM, ACCENT, FONT_FILENAME, FONT_URL
        global rgb_palette, luma_sorted_colors, hue_sorted_colors
        PALETTE_HEX = color_scheme['PALETTE_HEX']
        BG_COLOR = color_scheme['BG_COLOR']
        UI_BORDER = color_scheme['UI_BORDER']
        TEXT_COLOR = color_scheme['TEXT_MAIN']
        TEXT_DIM = color_scheme['TEXT_DIM']
        ACCENT = color_scheme['ACCENT']
        FONT_FILENAME = color_scheme['FONT_FILENAME']
        FONT_URL = color_scheme['FONT_URL']
        
        # Derived for this module
        rgb_palette = [tuple(int(PALETTE_HEX[i].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) for i in range(len(PALETTE_HEX))]
        
        luminance = [0.299*r + 0.587*g + 0.114*b for r,g,b in rgb_palette]
        luma_sorted_indices = np.argsort(luminance)
        luma_sorted_colors = [rgb_palette[i] for i in luma_sorted_indices]

        hues = [colorsys.rgb_to_hsv(r/255, g/255, b/255)[0] for r,g,b in rgb_palette]
        hue_sorted_indices = np.argsort(hues)
        hue_sorted_colors = [rgb_palette[i] for i in hue_sorted_indices]

    os.makedirs("images", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    study = PixelPerfectModule4V4()
    # Inject sorted colors into study instance since they are used as self.luma_sorted_colors etc.
    study.luma_sorted_colors = luma_sorted_colors
    study.hue_sorted_colors = hue_sorted_colors
    
    img = study.assemble(scale)
    img.save(OUTPUT_IMAGE)
    study.generate_markdown()
    print(f"Saved {OUTPUT_IMAGE}")
    print(f"MD Saved: {OUTPUT_MD}")

class PixelPerfectModule4V4:
    def __init__(self):
        pass

    def load_fonts(self, scale):
        if not os.path.exists(FONT_FILENAME):
            try: import urllib.request; urllib.request.urlretrieve(FONT_URL, FONT_FILENAME)
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

    def get_gray_match(self, rgb):
        lum = int(0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2])
        return (lum, lum, lum)

    def draw_neu_gray_diagonal(self, pixels, start_x, start_y, w, h, colors):
        """Row 1: Diagonal Split & Hue Sorted (Kept from V3)."""
        box_w = (w // len(colors)) - 1 
        for i, col in enumerate(colors):
            x_base = start_x + (i * (box_w + 1))
            gray = self.get_gray_match(col)
            for dy in range(h):
                split_dx = int((dy / (h-1)) * box_w)
                for dx in range(box_w):
                    px = x_base + dx
                    py = start_y + dy
                    if dx < (box_w - split_dx):
                         pixels[px, py] = col
                    else:
                        if (px + py) % 2 == 0: pixels[px, py] = col
                        else: pixels[px, py] = gray

    def draw_pal_row_scanline(self, pixels, start_x, start_y, w, h, colors):
        """
        Row 2 (CREATIVE REWORK): Scanline Texture.
        Alternates base color and slightly darker version per horizontal line.
        """
        box_w = w // len(colors)
        
        for i, col in enumerate(colors):
            x_start = start_x + (i * box_w)
            x_end = x_start + box_w
            
            # Pre-calculate scanline darkened color (e.g., 80% brightness)
            col_dark = tuple(int(c * 0.8) for c in col)
            
            # Draw Color Block with Scanline texture
            for py in range(start_y, start_y + h):
                # Determine if even or odd line relative to start of bar
                # We use a fixed 2-pixel pattern for scanlines
                is_even_line = (py // max(1, int(1))) % 2 == 0
                final_col = col if is_even_line else col_dark
                
                for px in range(x_start, x_end):
                    if px >= start_x + w: break
                    pixels[px, py] = final_col
            
            # Solid Separator
            if i < len(colors) - 1:
                sep_x = x_end - 1
                for py in range(start_y, start_y + h):
                    pixels[sep_x, py] = BG_COLOR

    def draw_hlf_row_specular(self, pixels, start_x, start_y, w, h, colors, scale):
        """
        Row 3 (CREATIVE REWORK): Specular Highlight Stack.
        Introduces a "highlight" step at the top, pushing base color down.
        """
        box_w = (w // len(colors)) - 1 
        h_thin = max(1, int(2 * scale))
        gap = max(1, int(1 * scale))
        
        y1_s, y1_e = 0, h_thin
        y2_s, y2_e = y1_e + gap, y1_e + gap + h_thin
        y3_s, y3_e = y2_e + gap, y2_e + gap + h_thin
        y4_s, y4_e = y3_e + gap, h
        
        for i, col in enumerate(colors):
            x = start_x + (i * (box_w + 1))
            
            # ---- NEW COLOR CALCULATIONS ----
            # 1. Highlight/Specular (mix 50% with white)
            c1 = tuple(int((c + 255)/2) for c in col)
            # 2. Base
            c2 = col
            # 3. Mid Shadow (70%)
            c3 = tuple(int(c * 0.70) for c in col)
            # 4. Deep Shadow (40%)
            c4 = tuple(int(c * 0.40) for c in col)
            
            def fill_rect(y_s, y_e, color):
                for dy in range(y_s, y_e):
                    if start_y + dy >= start_y + h: break
                    for dx in range(box_w):
                        if x + dx >= start_x + w: break
                        pixels[x + dx, start_y + dy] = color

            fill_rect(y1_s, y1_e, c1)
            fill_rect(y2_s, y2_e, c2)
            fill_rect(y3_s, y3_e, c3)
            fill_rect(y4_s, y4_e, c4)

    def draw_random_pairs(self, pixels, start_x, start_y, w, h, scale):
        """Row 4: Random Pairs Container (Vertical, 3 sections)."""
        num_pairs = 12
        gap = int(30 * scale) # Well separated
        pair_w = (w - (num_pairs - 1) * gap) // num_pairs
        
        h_sec = h // 3
        
        for i in range(num_pairs):
            x_start = start_x + i * (pair_w + gap)
            x_end = x_start + pair_w
            c1 = random.choice(rgb_palette)
            c2 = random.choice(rgb_palette)
            
            for dy in range(h):
                py = start_y + dy
                for dx in range(pair_w):
                    px = x_start + dx
                    
                    if dy < h_sec:
                        pixels[px, py] = c1
                    elif dy < 2 * h_sec:
                        # Interlaced mixture (checkerboard)
                        if (px + py) % 2 == 0:
                            pixels[px, py] = c1
                        else:
                            pixels[px, py] = c2
                    else:
                        pixels[px, py] = c2

    def assemble(self, scale=DEFAULT_SCALE):
        self.load_fonts(scale)
        w, h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
        margin, spacing = int(BASE_MARGIN * scale), int(BASE_SPACING * scale)
        canvas = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        pixels = canvas.load()

        # 1. Header
        title_text = "MODULE 4: THE MASTER STRIP"
        id_text = "ID: NORD_MOD4_PIXEL_V4"
        
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
        
        data_x = margin
        data_w = w - (2 * margin)
        
        # Row 1: NEU GRAY
        y1, h1 = content_y, int(40 * scale)
        self.draw_neu_gray_diagonal(pixels, data_x, y1, data_w, h1, self.hue_sorted_colors)
        self.draw_ui_element(draw, data_x, y1, data_w, h1, "NEU GRAY", "ID:21", scale)
        
        # Row 2: PAL
        y2 = y1 + h1 + spacing + int(20 * scale)
        h2 = int(20 * scale)
        self.draw_pal_row_scanline(pixels, data_x, y2, data_w, h2, self.luma_sorted_colors)
        self.draw_ui_element(draw, data_x, y2, data_w, h2, "PAL SCANLINE", "ID:22", scale)
        
        # Row 3: HLF
        y3 = y2 + h2 + spacing + int(20 * scale)
        h3 = int(40 * scale)
        self.draw_hlf_row_specular(pixels, data_x, y3, data_w, h3, self.luma_sorted_colors, scale)
        self.draw_ui_element(draw, data_x, y3, data_w, h3, "HLF SPECULAR", "ID:23", scale)

        # Row 4: RANDOM PAIRS
        y4 = y3 + h3 + spacing + int(20 * scale)
        h4 = int(120 * scale)
        self.draw_random_pairs(pixels, data_x, y4, data_w, h4, scale)
        self.draw_ui_element(draw, data_x, y4, data_w, h4, "RANDOM PAIRS", "ID:25", scale)

        return canvas

    def generate_markdown(self):
        md = f"""
# Module 4: The Master Strip (Creative Rework)
**Generated ID:** NORD_MOD4_PIXEL_V4

This version introduces creative textures and new data points to differentiate the rows visually.

## Row 1: NEU GRAY (Diagonal Hue Scan)
* **ID:21 (NEU GRAY):** Diagonal Split, sorted by Hue. Solid color vs Dithered Gray match.

## Row 2: PAL (Scanline Ramp)
* **ID:22 (PAL SCANLINE):** Continuous strip sorted by Luminance. Alternating horizontal lines show the base color and an 80% brightness version.

## Row 3: HLF (Specular Highlight Stack)
* **ID:23 (HLF SPECULAR):** Separated stacks sorted by Luminance. Top bar is a Highlight (Specular) tint.

## Row 4: RANDOM PAIRS
* **ID:25 (RANDOM PAIRS):** A collection of random color pairings from the palette to test contrast and harmony.
"""
        with open(OUTPUT_MD, "w") as f:
            f.write(md)
        print(f"MD Saved: {OUTPUT_MD}")

if __name__ == "__main__":
    run()
