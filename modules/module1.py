import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import os
import urllib.request

# ==========================================
# CONFIGURATION
# ==========================================
DEFAULT_SCALE = 1.0
OUTPUT_IMAGE = os.path.join("images", "module1.png")
OUTPUT_MD = os.path.join("reports", "module1.md")

# Base Dimensions (At Scale 1.0)
BASE_WIDTH = 1470
BASE_HEIGHT = 500
BASE_MARGIN = 40
BASE_PANEL_W = 350
BASE_PANEL_H = 300
BASE_BAR_W = 50
BASE_SPACING = 20

# Configuration inherited from main.py
PALETTE_HEX = []
BG_COLOR = (0, 0, 0)
UI_BORDER = (0, 0, 0)
TEXT_MAIN = (0, 0, 0)
TEXT_DIM = (0, 0, 0)
ACCENT = (0, 0, 0)
FONT_FILENAME = ""
FONT_URL = ""

def run(scale=DEFAULT_SCALE, color_scheme=None):
    if color_scheme:
        global PALETTE_HEX, BG_COLOR, UI_BORDER, TEXT_MAIN, TEXT_DIM, ACCENT, FONT_FILENAME, FONT_URL
        PALETTE_HEX = color_scheme['PALETTE_HEX']
        BG_COLOR = color_scheme['BG_COLOR']
        UI_BORDER = color_scheme['UI_BORDER']
        TEXT_MAIN = color_scheme['TEXT_MAIN']
        TEXT_DIM = color_scheme['TEXT_DIM']
        ACCENT = color_scheme['ACCENT']
        FONT_FILENAME = color_scheme['FONT_FILENAME']
        FONT_URL = color_scheme['FONT_URL']

    os.makedirs("images", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    study = IndustrialColorStudy(PALETTE_HEX)
    img = study.assemble(scale)
    img.save(OUTPUT_IMAGE)
    study.generate_markdown()
    print(f"Saved {OUTPUT_IMAGE}")

class IndustrialColorStudy:
    def __init__(self, palette_hex):
        self.palette_hex = palette_hex
        self.rgb_colors = np.array([self.hex_to_rgb_norm(c) for c in palette_hex])
        self.luminance = np.array([0.299*r + 0.587*g + 0.114*b for r,g,b in self.rgb_colors])

    def hex_to_rgb_norm(self, hex_str):
        hex_str = hex_str.lstrip('#')
        return [int(hex_str[i:i+2], 16)/255.0 for i in (0, 2, 4)]

    def load_fonts(self, scale):
        if not os.path.exists(FONT_FILENAME):
            try: urllib.request.urlretrieve(FONT_URL, FONT_FILENAME)
            except: pass
        
        size_main = int(max(6, 14 * scale))
        size_header = int(max(10, 24 * scale))
        size_tiny = int(max(5, 10 * scale))

        try:
            self.font_main = ImageFont.truetype(FONT_FILENAME, size_main)
            self.font_header = ImageFont.truetype(FONT_FILENAME, size_header)
            self.font_tiny = ImageFont.truetype(FONT_FILENAME, size_tiny)
        except:
            self.font_main = ImageFont.load_default()
            self.font_header = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

    def hsv_to_rgb_vectorized(self, h, s, v):
        c = v * s
        x = c * (1 - np.abs((h * 6) % 2 - 1))
        m = v - c
        z = np.zeros_like(h)
        cond = (h * 6).astype(int)
        
        r = np.select([cond == 0, cond == 1, cond == 2, cond == 3, cond == 4, cond == 5],
                      [c, x, z, z, x, c], default=z)
        g = np.select([cond == 0, cond == 1, cond == 2, cond == 3, cond == 4, cond == 5],
                      [x, c, c, x, z, z], default=z)
        b = np.select([cond == 0, cond == 1, cond == 2, cond == 3, cond == 4, cond == 5],
                      [z, z, x, c, c, x], default=z)
        return np.dstack((r+m, g+m, b+m))

    def generate_voronoi_slice(self, w, h, target_sat):
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        xv, yv = np.meshgrid(x, y)
        target_val = yv 
        target_sat_mat = np.full_like(xv, target_sat)
        target_rgb = self.hsv_to_rgb_vectorized(xv, target_sat_mat, target_val)
        
        diff = target_rgb[:, :, np.newaxis, :] - self.rgb_colors[np.newaxis, np.newaxis, :, :]
        dist_sq = np.sum(diff**2, axis=3)
        closest_indices = np.argmin(dist_sq, axis=2)
        
        img_arr = self.rgb_colors[closest_indices]
        return Image.fromarray((img_arr * 255).astype(np.uint8))

    def draw_ui_element(self, draw, x, y, w, h, title, subtitle, scale):
        text_padding = int(5 * scale)
        title_y = y - int(22 * scale) 
        draw.text((x, title_y), title, fill=TEXT_MAIN, font=self.font_main)
        
        sub_bbox = draw.textbbox((0, 0), subtitle, font=self.font_tiny)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_y = y + h + text_padding
        draw.text((x + w - sub_w, sub_y), subtitle, fill=TEXT_DIM, font=self.font_tiny)
        
        border_width = max(1, int(1 * scale))
        draw.rectangle([x-1, y-1, x+w, y+h], outline=UI_BORDER, width=border_width)

    def create_sorted_bar(self, w, h, mode="ref"):
        if mode == "raw":
            indices = range(len(self.rgb_colors))
        else:
            indices = np.argsort(self.luminance)
            
        img = Image.new('RGB', (w, h))
        draw = ImageDraw.Draw(img)
        bh = h / len(self.rgb_colors)
        
        for i, idx in enumerate(indices):
            col = self.rgb_colors[idx]
            if mode == "gray":
                lum = 0.299*col[0] + 0.587*col[1] + 0.114*col[2]
                final_col = (lum, lum, lum)
            elif mode == "sat_max":
                h_val, s_val, v_val = colorsys.rgb_to_hsv(*col)
                if s_val < 0.1: final_col = col 
                else: final_col = colorsys.hsv_to_rgb(h_val, 1.0, v_val)
            else: 
                final_col = col

            y0 = int(i * bh)
            y1 = int((i+1) * bh)
            draw.rectangle([0, y0, w, y1], fill=tuple(int(c*255) for c in final_col))
        return img

    def assemble(self, scale=DEFAULT_SCALE):
        self.load_fonts(scale)
        w, h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
        margin, spacing = int(BASE_MARGIN * scale), int(BASE_SPACING * scale)
        panel_w = int(BASE_PANEL_W * scale)
        panel_h = int(BASE_PANEL_H * scale)
        bar_w = int(BASE_BAR_W * scale)

        canvas = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        # 1. Header
        title_text = "MODULE 1: ALIGNED LINEAR ANALYSIS"
        id_text = "ID: NORD_MOD1_LINEAR"
        
        # Title (Top Left)
        draw.text((margin, margin), title_text, fill=TEXT_MAIN, font=self.font_header)
        
        # ID (Top Right)
        id_bbox = draw.textbbox((0, 0), id_text, font=self.font_tiny)
        id_w = id_bbox[2] - id_bbox[0]
        draw.text((w - margin - id_w, margin + int(5 * scale)), id_text, fill=TEXT_DIM, font=self.font_tiny)
        
        # Line
        line_y = margin + int(40 * scale)
        draw.line([(margin, line_y), (w - margin, line_y)], fill=UI_BORDER, width=max(1, int(1 * scale)))
        
        content_y = line_y + spacing + int(20 * scale)
        cursor_x = margin
        
        # --- 1. COLUMNS ---
        for mode, label, id_str in [("raw", "RAW", "ID:00"), ("gray", "LUM", "ID:01"), ("ref", "REF", "ID:02"), ("sat_max", "SAT+", "ID:03")]:
            bar = self.create_sorted_bar(bar_w, panel_h, mode)
            canvas.paste(bar, (cursor_x, content_y))
            self.draw_ui_element(draw, cursor_x, content_y, bar_w, panel_h, label, id_str, scale)
            cursor_x += bar_w + spacing
        
        cursor_x += spacing # Extra gap
        
        # --- 2. VORONOI PLOTS ---
        for s_val, label, id_str in [(1.0, "PURE", "S:1.0"), (0.5, "MID", "S:0.5"), (0.2, "MUTE", "S:0.2")]:
            v = self.generate_voronoi_slice(panel_w, panel_h, s_val)
            canvas.paste(v, (cursor_x, content_y))
            self.draw_ui_element(draw, cursor_x, content_y, panel_w, panel_h, label, id_str, scale)
            cursor_x += panel_w + spacing

        return canvas

    def generate_markdown(self):
        md_content = f"""
# Color Study Analysis: Nord Palette
**Generated ID:** NORD_MOD1_INDUSTRIAL

## 1. Structure Columns (Left)
* **ID:00 (RAW):** The palette in its original definition order.
* **ID:01 (LUM):** Grayscale sort (Dark to Light).
* **ID:02 (REF):** Natural color sort (Dark to Light).
* **ID:03 (SAT+):** Forced saturation.

## 2. Saturation Models (Right)
Voronoi diagrams showing which palette color is the nearest match for a given Hue (X) and Brightness (Y).
* **PURE (S:1.0):** How the palette handles neon/bright environments.
* **MID (S:0.5):** How the palette handles standard lighting.
* **MUTE (S:0.2):** How the palette handles foggy/dull environments.
"""
        with open(OUTPUT_MD, "w") as f:
            f.write(md_content)
        print(f"Markdown saved to {OUTPUT_MD}")

if __name__ == "__main__":
    run()
