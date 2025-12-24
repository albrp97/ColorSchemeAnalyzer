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
OUTPUT_IMAGE = os.path.join("images", "module6.png")

# Base Dimensions (At Scale 1.0)
BASE_WIDTH = 1600
BASE_HEIGHT = 1000
BASE_MARGIN = 40
BASE_SPACING = 20
# Configuration inherited from main.py
PALETTE_HEX = []
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
UI_BORDER = (0, 0, 0)
TEXT_DIM = (0, 0, 0)
ACCENT = (0, 0, 0)
FONT_FILENAME = ""
FONT_URL = ""
rgb_palette = []
palette_arr = np.array([])

def run(scale=DEFAULT_SCALE, color_scheme=None, output_image=None):
    if color_scheme:
        global PALETTE_HEX, BG_COLOR, TEXT_COLOR, UI_BORDER, TEXT_DIM, ACCENT, FONT_FILENAME, FONT_URL, rgb_palette, palette_arr
        PALETTE_HEX = color_scheme['PALETTE_HEX']
        BG_COLOR = color_scheme['BG_COLOR']
        TEXT_COLOR = color_scheme['TEXT_MAIN']
        UI_BORDER = color_scheme['UI_BORDER']
        TEXT_DIM = color_scheme['TEXT_DIM']
        ACCENT = color_scheme['ACCENT']
        FONT_FILENAME = color_scheme['FONT_FILENAME']
        FONT_URL = color_scheme['FONT_URL']
        rgb_palette = [tuple(int(PALETTE_HEX[i].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) for i in range(len(PALETTE_HEX))]
        palette_arr = np.array(rgb_palette)

    out_img = output_image if output_image else OUTPUT_IMAGE

    os.makedirs(os.path.dirname(out_img), exist_ok=True)
    study = Module6SwappedGamut()
    img = study.assemble(scale)
    img.save(out_img)
    print(f"Saved {out_img}")

class Module6SwappedGamut:
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

    # --- RENDERER 1: FISHEYE (Now for Bottom Spheres) ---
    def render_fisheye_sphere(self, pixels, center_x, center_y, radius, fixed_sat_0_1, canvas_w, canvas_h):
        x0 = max(0, int(center_x - radius))
        x1 = min(canvas_w, int(center_x + radius + 1))
        y0 = max(0, int(center_y - radius))
        y1 = min(canvas_h, int(center_y + radius + 1))
        r_sq = radius * radius
        ambient = 0.1

        for y in range(y0, y1):
            for x in range(x0, x1):
                dx = x - center_x
                dy = y - center_y
                dist_sq = dx*dx + dy*dy
                if dist_sq > r_sq: continue

                # Fisheye Distortion logic
                r_lin = math.sqrt(dist_sq) / radius
                r_fish = math.asin(r_lin) / (math.pi / 2)
                
                # Brightness (Center=Bright)
                V = ambient + (1.0 - ambient) * (1.0 - r_fish)
                # Hue (Angle)
                H = (math.atan2(dy, dx) + math.pi) / (2 * math.pi)
                # Saturation (Fixed)
                S = fixed_sat_0_1

                r_th, g_th, b_th = colorsys.hsv_to_rgb(H, S, V)
                idx = self.get_closest_color_fast(int(r_th*255), int(g_th*255), int(b_th*255))
                pixels[x, y] = rgb_palette[idx]

    # --- RENDERER 2: 3D LIT (Now for Top Spheres) ---
    def render_3d_gamut_sphere(self, pixels, center_x, center_y, radius, fixed_sat_0_1, canvas_w, canvas_h):
        lx, ly, lz = -0.6, -0.6, 0.8 # Light top-left
        lm = math.sqrt(lx*lx + ly*ly + lz*lz)
        lx, ly, lz = lx/lm, ly/lm, lz/lm
        ambient = 0.25 

        x0 = max(0, int(center_x - radius))
        x1 = min(canvas_w, int(center_x + radius + 1))
        y0 = max(0, int(center_y - radius))
        y1 = min(canvas_h, int(center_y + radius + 1))
        r_sq = radius * radius

        for y in range(y0, y1):
            for x in range(x0, x1):
                dx = x - center_x
                dy = y - center_y
                dist_sq = dx*dx + dy*dy
                if dist_sq > r_sq: continue

                # 3D Normal & Lighting
                nx = dx / radius
                ny = dy / radius
                nz = math.sqrt(max(0.0, 1.0 - nx*nx - ny*ny))
                diffuse = max(0.0, nx*lx + ny*ly + nz*lz)
                
                V = min(1.0, max(0.0, ambient + (1.0 - ambient) * diffuse))
                H = (math.atan2(dy, dx) + math.pi) / (2 * math.pi)
                S = fixed_sat_0_1

                r_th, g_th, b_th = colorsys.hsv_to_rgb(H, S, V)
                idx = self.get_closest_color_fast(int(r_th*255), int(g_th*255), int(b_th*255))
                pixels[x, y] = rgb_palette[idx]

    def assemble(self, scale=DEFAULT_SCALE):
        self.load_fonts(scale)
        w, h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
        margin, spacing = int(BASE_MARGIN * scale), int(BASE_SPACING * scale)
        canvas = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        pixels = canvas.load()
        
        # 1. Header
        title_text = "MODULE 6: HYBRID GAMUT"
        id_text = "ID: NORD_MOD6_SWAPPED"
        
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
        box_w = (w - (2 * margin) - spacing) // 2
        box_h = (h - content_y - margin - spacing) // 2
        
        # --- TOP ROW: 3D LIT SPHERES ---
        
        # SPHERE 1: Top Left
        x1, y1 = margin, content_y
        self.render_3d_gamut_sphere(pixels, x1 + box_w//2, y1 + box_h//2, min(box_w, box_h)//2 - int(10 * scale), 0.6, w, h)
        self.draw_ui_element(draw, x1, y1, box_w, box_h, "LIT SPHERE (S:60%)", "ID:26", scale)

        # SPHERE 2: Top Right
        x2, y2 = margin + box_w + spacing, content_y
        self.render_3d_gamut_sphere(pixels, x2 + box_w//2, y2 + box_h//2, min(box_w, box_h)//2 - int(10 * scale), 0.8, w, h)
        self.draw_ui_element(draw, x2, y2, box_w, box_h, "LIT SPHERE (S:80%)", "ID:27", scale)

        # --- BOTTOM ROW: FISHEYE SPHERES ---

        # SPHERE 3: Bottom Left
        x3, y3 = margin, content_y + box_h + spacing + int(20 * scale)
        self.render_fisheye_sphere(pixels, x3 + box_w//2, y3 + box_h//2, min(box_w, box_h)//2 - int(10 * scale), 1.0, w, h)
        self.draw_ui_element(draw, x3, y3, box_w, box_h, "FISH SPHERE (S:100%)", "ID:28", scale)

        # SPHERE 4: Bottom Right
        x4, y4 = margin + box_w + spacing, content_y + box_h + spacing + int(20 * scale)
        self.render_fisheye_sphere(pixels, x4 + box_w//2, y4 + box_h//2, min(box_w, box_h)//2 - int(10 * scale), 96/255.0, w, h)
        self.draw_ui_element(draw, x4, y4, box_w, box_h, "FISH SPHERE (S:37%)", "ID:29", scale)

        return canvas

if __name__ == "__main__":
    run()
