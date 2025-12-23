import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import os
import urllib.request

# ==========================================
# CONFIGURATION
# ==========================================
DEFAULT_SCALE = 1.0
OUTPUT_IMAGE = os.path.join("images", "module2.png")
OUTPUT_MD = os.path.join("reports", "module2.md")

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
    study = FinalLinearStudy(PALETTE_HEX)
    img = study.assemble(scale)
    img.save(OUTPUT_IMAGE)
    study.generate_markdown()
    print(f"Saved {OUTPUT_IMAGE}")

# Base Dimensions (At Scale 1.0)
BASE_WIDTH = 1600
BASE_MARGIN = 40
BASE_SPACING = 20
BASE_TEXT_PADDING = 8

class FinalLinearStudy:
    def __init__(self, palette_hex):
        self.palette_hex = palette_hex
        self.rgb_colors = np.array([self.hex_to_rgb_norm(c) for c in palette_hex])
        self.luminance = np.array([0.299*r + 0.587*g + 0.114*b for r,g,b in self.rgb_colors])

    def hex_to_rgb_norm(self, hex_str):
        h = hex_str.lstrip('#')
        return [int(h[i:i+2], 16)/255.0 for i in (0, 2, 4)]

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

    def render_bar_blocks(self, w, h, colors):
        img = Image.new('RGB', (w, h))
        draw = ImageDraw.Draw(img)
        cw = w / len(colors)
        for i, col in enumerate(colors):
            x0 = int(i * cw)
            x1 = int((i+1) * cw)
            draw.rectangle([x0, 0, x1, h], fill=tuple(int(c*255) for c in col))
        return img

    def render_bar_gradient(self, w, h, colors):
        arr = np.zeros((1, w, 3))
        n = len(colors)
        for x in range(w):
            pos = (x / (w - 1)) * (n - 1)
            idx1 = int(np.floor(pos))
            idx2 = int(np.ceil(pos))
            blend = pos - idx1
            c1 = np.array(colors[idx1])
            c2 = np.array(colors[idx2])
            mixed = (1 - blend) * c1 + blend * c2
            arr[0, x] = mixed
        img_strip = Image.fromarray((arr * 255).astype(np.uint8))
        return img_strip.resize((w, h), Image.NEAREST)

    def get_filtered_palette(self, mode):
        new_cols = []
        for col in self.rgb_colors:
            h, s, v = colorsys.rgb_to_hsv(*col)
            if mode == "b65": new_col = colorsys.hsv_to_rgb(h, s, 0.65)
            elif mode == "b10": new_col = colorsys.hsv_to_rgb(h, s, 0.10)
            elif mode == "s50": new_col = colorsys.hsv_to_rgb(h, 0.50, v)
            elif mode == "l50": 
                h_l, l_l, s_l = colorsys.rgb_to_hls(*col)
                new_col = colorsys.hls_to_rgb(h_l, 0.50, s_l)
            else: new_col = col
            new_cols.append(new_col)
        return new_cols

    def render_close_grid(self, w, h, threshold_percent, scale):
        img = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        matches = []
        indices = np.argsort(self.luminance)
        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                idx1, idx2 = indices[i], indices[j]
                diff = abs(self.luminance[idx1] - self.luminance[idx2])
                if diff <= threshold_percent:
                    matches.append((self.rgb_colors[idx1], self.rgb_colors[idx2]))

        if not matches:
            draw.text((0,0), "NO MATCHES", fill=TEXT_MAIN, font=self.font_label)
            return img

        pair_w = int(60 * scale)
        row_h = int(30 * scale)
        
        x, y = 0, 0
        for c1, c2 in matches:
            if y + row_h > h: break 
            
            draw.rectangle([x, y, x + pair_w//2, y + row_h], fill=tuple(int(c*255) for c in c1))
            draw.rectangle([x + pair_w//2, y, x + pair_w, y + row_h], fill=tuple(int(c*255) for c in c2))
            
            x += pair_w
            if x + pair_w > w:
                x = 0
                y += row_h + int(2 * scale) 

        return img

    def assemble(self, scale=DEFAULT_SCALE):
        self.load_fonts(scale)
        w = int(BASE_WIDTH * scale)
        margin = int(BASE_MARGIN * scale)
        spacing = int(BASE_SPACING * scale)
        
        # 1. Header Logic
        title_text = "MODULE 2: ALIGNED LINEAR ANALYSIS"
        id_text = "ID: NORD_MOD2_V8"
        
        # Line
        line_y = margin + int(40 * scale)
        content_y = line_y + spacing + int(20 * scale)

        # 2. CALCULATE HEIGHTS
        h_filter_bar = int(25 * scale)
        h_filter_stack = (h_filter_bar * 4) 
        gap_stacks = int(40 * scale)
        
        h_label = int(20 * scale) 
        h_main_bar = int(50 * scale)
        h_main_unit = h_label + h_main_bar 
        gap_main_items = int(30 * scale) 
        
        total_content_height = h_filter_stack + gap_stacks + (4 * h_main_unit) + (3 * gap_main_items)
        
        h_indexed = int(100 * scale)
        gap_right = int(40 * scale) 
        total_label_height_right = (3 * h_label)
        h_remaining = total_content_height - h_indexed - total_label_height_right - (2 * gap_right)
        h_match_grid = h_remaining // 2

        canvas_h = content_y + total_content_height + margin
        
        canvas = Image.new('RGB', (w, canvas_h), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        # DRAW HEADER
        draw.text((margin, margin), title_text, fill=TEXT_MAIN, font=self.font_header)
        id_bbox = draw.textbbox((0, 0), id_text, font=self.font_tiny)
        id_w = id_bbox[2] - id_bbox[0]
        draw.text((w - margin - id_w, margin + int(5 * scale)), id_text, fill=TEXT_DIM, font=self.font_tiny)
        draw.line([(margin, line_y), (w - margin, line_y)], fill=UI_BORDER, width=max(1, int(1 * scale)))

        # --- DRAW LEFT COLUMN ---
        col1_x = margin + int(60 * scale) 
        col1_y = content_y
        col1_w = int(w * 0.60) - int(60 * scale)
        
        curr_y = col1_y
        
        # A. Filter Stack
        filters = [("b65%", "b65"), ("b10%", "b10"), ("S50", "s50"), ("L50", "l50")]
        filter_img = Image.new('RGB', (col1_w, h_filter_stack))
        fi_draw = ImageDraw.Draw(filter_img)
        fy = 0
        for label, mode in filters:
            bar = self.render_bar_blocks(col1_w, h_filter_bar, self.get_filtered_palette(mode))
            filter_img.paste(bar, (0, fy))
            fy += h_filter_bar
        
        canvas.paste(filter_img, (col1_x, curr_y))
        self.draw_ui_element(draw, col1_x, curr_y, col1_w, h_filter_stack, "FILTER STACK", "ID:04", scale)
        
        fy = curr_y
        for label, mode in filters:
            # Center text vertically in the bar
            ascent, descent = self.font_tiny.getmetrics()
            font_h = ascent + descent
            ly = fy + (h_filter_bar // 2) - (font_h // 2)
            draw.text((margin, ly), label, fill=TEXT_DIM, font=self.font_tiny)
            fy += h_filter_bar

        curr_y += h_filter_stack + gap_stacks
        
        # B. Main Stack
        main_sections = [
            ("RAW PALETTE", self.render_bar_blocks(col1_w, h_main_bar, self.rgb_colors), "ID:05"),
            ("LUMA SORT", self.render_bar_blocks(col1_w, h_main_bar, self.rgb_colors[np.argsort(self.luminance)]), "ID:06"),
            ("HUE RAMP (SMOOTH)", self.render_bar_gradient(col1_w, h_main_bar, sorted(self.rgb_colors, key=lambda c: colorsys.rgb_to_hsv(*c)[0])), "ID:07"),
            ("LUMA RAMP (SMOOTH)", self.render_bar_gradient(col1_w, h_main_bar, self.rgb_colors[np.argsort(self.luminance)]), "ID:08")
        ]

        for title, img, mod_id in main_sections:
            canvas.paste(img, (col1_x, curr_y))
            self.draw_ui_element(draw, col1_x, curr_y, col1_w, h_main_bar, title, mod_id, scale)
            curr_y += h_main_bar + gap_main_items

        # --- DRAW RIGHT COLUMN ---
        col2_x = col1_x + col1_w + spacing
        col2_y = col1_y
        col2_w = w - col2_x - margin
        
        curr_y = col2_y
        
        # 1. Indexed Grid
        grid_img = Image.new('RGB', (col2_w, h_indexed))
        gd = ImageDraw.Draw(grid_img)
        rows, cols = 4, 4
        cw, ch = col2_w/cols, h_indexed/rows
        for i, c in enumerate(self.rgb_colors):
            r, cl = i//cols, i%cols
            gd.rectangle([cl*cw, r*ch, (cl+1)*cw, (r+1)*ch], fill=tuple(int(x*255) for x in c))
        
        canvas.paste(grid_img, (col2_x, curr_y))
        self.draw_ui_element(draw, col2_x, curr_y, col2_w, h_indexed, "INDEXED: 4x4", "ID:09", scale)
        curr_y += h_indexed + gap_right
        
        # 2. Close Match 10%
        m10 = self.render_close_grid(col2_w, h_match_grid, 0.10, scale)
        canvas.paste(m10, (col2_x, curr_y))
        self.draw_ui_element(draw, col2_x, curr_y, col2_w, h_match_grid, "CLOSE MATCHES: 10% (TIGHT)", "ID:10", scale)
        curr_y += h_match_grid + gap_right

        # 3. Close Match 30%
        m30 = self.render_close_grid(col2_w, h_match_grid, 0.30, scale)
        canvas.paste(m30, (col2_x, curr_y))
        self.draw_ui_element(draw, col2_x, curr_y, col2_w, h_match_grid, "CLOSE MATCHES: 30% (LOOSE)", "ID:11", scale)
        
        return canvas

    def generate_markdown(self):
        md = f"""
# Module 2: Aligned Linear Analysis (Final)
**Generated ID:** NORD_MOD2_V8

## 1. Filter Stack (Top Left)
* **ID:04 (FILTER STACK):** Shows the palette under various constraints (Brightness 65%, 10%, Saturation 50%, Luminance 50%).

## 2. Main Stack (Bottom Left)
* **ID:05 (RAW PALETTE):** The palette in its original definition order.
* **ID:06 (LUMA SORT):** Sorted by luminance.
* **ID:07 (HUE RAMP):** Smooth gradient sorted by hue.
* **ID:08 (LUMA RAMP):** Smooth gradient sorted by luminance.

## 3. Distribution & Matching (Right)
* **ID:09 (INDEXED: 4x4):** 4x4 grid of the palette.
* **ID:10 (CLOSE MATCHES: 10%):** Pairs of colors with less than 10% luminance difference.
* **ID:11 (CLOSE MATCHES: 30%):** Pairs of colors with less than 30% luminance difference.
"""
        with open(OUTPUT_MD, "w") as f:
            f.write(md)
        print(f"Markdown saved to {OUTPUT_MD}")

if __name__ == "__main__":
    run()
