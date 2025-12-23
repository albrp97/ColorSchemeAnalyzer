import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import math
import io
import os
import urllib.request

# ==========================================
# CONFIGURATION
# ==========================================
DEFAULT_SCALE = 1.0
OUTPUT_IMAGE = os.path.join("images", "module5.png")
OUTPUT_MD = os.path.join("reports", "module5.md")

# Configuration inherited from main.py
PALETTE_HEX = []
BG_COLOR_RGB = (0, 0, 0)
BG_COLOR_HEX = "#000000"
TEXT_COLOR_RGB = (0, 0, 0)
PLOT_BG_RGB = (0, 0, 0)
UI_BORDER = (0, 0, 0)
TEXT_DIM = (0, 0, 0)
ACCENT = (0, 0, 0)
FONT_FILENAME = ""
FONT_URL = ""
rgb_palette = []

# Base Dimensions (At Scale 1.0)
BASE_WIDTH = 600
BASE_HEIGHT = 1300 
BASE_MARGIN = 40
BASE_SPACING = 20

def run(scale=DEFAULT_SCALE, color_scheme=None):
    if color_scheme:
        global PALETTE_HEX, BG_COLOR_RGB, BG_COLOR_HEX, TEXT_COLOR_RGB, PLOT_BG_RGB, UI_BORDER, TEXT_DIM, ACCENT, FONT_FILENAME, FONT_URL, rgb_palette
        PALETTE_HEX = color_scheme['PALETTE_HEX']
        BG_COLOR_RGB = color_scheme['BG_COLOR']
        BG_COLOR_HEX = '#%02x%02x%02x' % BG_COLOR_RGB
        TEXT_COLOR_RGB = color_scheme['TEXT_MAIN']
        PLOT_BG_RGB = color_scheme['PLOT_BG']
        UI_BORDER = color_scheme['UI_BORDER']
        TEXT_DIM = color_scheme['TEXT_DIM']
        ACCENT = color_scheme['ACCENT']
        FONT_FILENAME = color_scheme['FONT_FILENAME']
        FONT_URL = color_scheme['FONT_URL']
        rgb_palette = [tuple(int(PALETTE_HEX[i].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) for i in range(len(PALETTE_HEX))]

    os.makedirs("images", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    study = Module5Normalized()
    img = study.assemble(scale)
    img.save(OUTPUT_IMAGE)
    study.generate_markdown()
    print(f"Saved {OUTPUT_IMAGE}")

# ==========================================
# 1. MATPLOTLIB GENERATOR (4x4 Grid)
# ==========================================
def generate_contour_grid(width_px, height_px):
    rows = 4
    cols = 4
    resolution = 50 

    dpi = 100
    fig_w = width_px / dpi
    fig_h = height_px / dpi
    
    fig, axes = plt.subplots(rows, cols, figsize=(fig_w, fig_h), dpi=dpi)
    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, top=1, bottom=0)
    fig.patch.set_facecolor(BG_COLOR_HEX)

    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y)

    def generate_radial_sweep(x_grid, y_grid, step, total_steps):
        center_x = -0.5 + (step / total_steps) * 2.0
        center_y = 0.5
        dist = np.sqrt((x_grid - center_x)**2 + (y_grid - center_y)**2)
        z = dist + 0.1 * np.sin(10 * x_grid)
        return z

    def generate_random_blobs(x_grid, y_grid, seed):
        np.random.seed(seed)
        z = np.zeros_like(x_grid)
        for _ in range(3):
            freq_x = np.random.uniform(2, 6)
            freq_y = np.random.uniform(2, 6)
            phase_x = np.random.uniform(0, 2*np.pi)
            phase_y = np.random.uniform(0, 2*np.pi)
            z += np.sin(freq_x * x_grid + phase_x) * np.cos(freq_y * y_grid + phase_y)
        return z

    for i, ax in enumerate(axes.flat):
        if i >= len(PALETTE_HEX): 
            # Fill empty squares with random colors from the palette
            color_hex = np.random.choice(PALETTE_HEX)
        else:
            color_hex = PALETTE_HEX[i]

        cmap = mcolors.LinearSegmentedColormap.from_list("nord_gradient", [BG_COLOR_HEX, color_hex])
        
        if i < 8:
            Z = -generate_radial_sweep(X, Y, i, 8)
            levels = 7
        else:
            Z = generate_random_blobs(X, Y, seed=(i + 10) * 42)
            levels = 6

        ax.contourf(X, Y, Z, levels=levels, cmap=cmap)
        ax.axis('off')
        ax.set_aspect('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=BG_COLOR_HEX)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# ==========================================
# 2. PIL ASSEMBLER
# ==========================================
class Module5Normalized:
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
        text_padding = int(5 * scale)
        title_y = y - int(22 * scale) 
        draw.text((x, title_y), title, fill=TEXT_COLOR_RGB, font=self.font)
        
        sub_bbox = draw.textbbox((0, 0), subtitle, font=self.font_tiny)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_y = y + h + text_padding
        draw.text((x + w - sub_w, sub_y), subtitle, fill=TEXT_DIM, font=self.font_tiny)
        
        border_width = max(1, int(1 * scale))
        draw.rectangle([x-1, y-1, x+w, y+h], outline=UI_BORDER, width=border_width)

    def draw_polar_plot_normalized(self, canvas, center_x, center_y, radius, colors, scale):
        if radius < 1: radius = 1
        
        # Create a separate image for the polar plot to handle clipping automatically
        plot_size = int(radius * 2)
        plot_img = Image.new('RGBA', (plot_size, plot_size), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(plot_img)
        
        # Draw background lines on the plot_img
        mid = radius
        p_draw.line([0, mid, plot_size, mid], fill=PLOT_BG_RGB + (255,))
        p_draw.line([mid, 0, mid, plot_size], fill=PLOT_BG_RGB + (255,))
        p_draw.rectangle([0, 0, plot_size-1, plot_size-1], outline=PLOT_BG_RGB + (255,))

        hsv_colors = []
        max_s = 0.0
        for col in colors:
            r, g, b = col[0]/255, col[1]/255, col[2]/255
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            hsv_colors.append((h, s, v))
            if s > max_s:
                max_s = s
        
        if max_s <= 0.001: max_s = 1.0 
        dot_radius = int(120 * scale) # Increased radius for bigger circles

        # Pre-calculate positions to allow layered rendering for better color mixing
        positions = []
        for i, col in enumerate(colors):
            h, s, v = hsv_colors[i]
            angle = (h * 2 * math.pi) - (math.pi / 2)
            s_norm = s / max_s
            dist = s_norm * radius
            px = mid + (dist * math.cos(angle))
            py = mid + (dist * math.sin(angle))
            positions.append((px, py, col))

        # Draw in layers: all outer "glows" first, then progressively smaller/more opaque cores.
        # This ensures that the overlapping fringes of different colors mixture together
        # rather than one color's core simply overwriting another's fringe.
        steps = 20
        for step in range(steps):
            # step 0 is outer (largest), step steps-1 is inner (smallest)
            r_step = dot_radius * (1 - step/steps)
            # Alpha increases as we go towards the center
            # Slightly lower base alpha for better blending of larger areas
            alpha = int(5 + (150 * (step/steps)**2.0))
            
            for px, py, col in positions:
                fill_col = col + (alpha,)
                p_draw.ellipse([px - r_step, py - r_step, px + r_step, py + r_step], fill=fill_col)
        
        # Final pass for the bright cores
        for px, py, col in positions:
            core_r = max(1, int(3 * scale))
            p_draw.ellipse([px - core_r, py - core_r, px + core_r, py + core_r], fill=(255, 255, 255, 180))

        # Paste the plot_img onto the main canvas
        canvas.paste(plot_img, (int(center_x - radius), int(center_y - radius)), plot_img)

    def assemble(self, scale=DEFAULT_SCALE):
        self.load_fonts(scale)
        w, h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
        margin, spacing = int(BASE_MARGIN * scale), int(BASE_SPACING * scale)
        
        canvas = Image.new('RGB', (w, h), BG_COLOR_RGB)
        draw = ImageDraw.Draw(canvas)
        
        # 1. Header
        title_text = "MODULE 5: CONTOUR & POLAR"
        id_text = "ID: NORD_MOD5_CONTOUR"
        
        # Title (Top Left)
        draw.text((margin, margin), title_text, fill=TEXT_COLOR_RGB, font=self.font)
        
        # ID (Top Right)
        id_bbox = draw.textbbox((0, 0), id_text, font=self.font_tiny)
        id_w = id_bbox[2] - id_bbox[0]
        draw.text((w - margin - id_w, margin + int(5 * scale)), id_text, fill=TEXT_DIM, font=self.font_tiny)
        
        # Line
        line_y = margin + int(40 * scale)
        draw.line([(margin, line_y), (w - margin, line_y)], fill=UI_BORDER, width=max(1, int(1 * scale)))
        
        content_y = line_y + spacing + int(20 * scale)
        
        # --- TOP: 4x4 CONTOUR GRID ---
        grid_width = w - (2 * margin)
        grid_height = grid_width 
        
        contour_img = generate_contour_grid(grid_width, grid_height)
        canvas.paste(contour_img, (margin, content_y))
        self.draw_ui_element(draw, margin, content_y, grid_width, grid_height, "12-BIT COLSPACE", "ID:24", scale)
        
        curr_y = content_y + grid_height + spacing + int(40 * scale)
        
        # --- BOTTOM: POLAR PLOT ---
        polar_radius = grid_width // 2
        polar_center_x = w // 2
        polar_center_y = curr_y + polar_radius
        
        self.draw_polar_plot_normalized(canvas, polar_center_x, polar_center_y, polar_radius, rgb_palette, scale)
        self.draw_ui_element(draw, polar_center_x - polar_radius, curr_y, polar_radius*2, polar_radius*2, "POLAR_SAT", "ID:P01", scale)

        return canvas

    def generate_markdown(self):
        md_content = f"""
# Contour & Polar Analysis: Nord Palette
**Generated ID:** NORD_MOD5_CONTOUR

## 1. 12-Bit Colspace (Top)
A 4x4 grid of contour plots. Each cell represents one color from the Nord palette, showing its interaction with the background color.
* **Top 8:** Radial sweeps.
* **Bottom 8:** Random blob interference patterns.

## 2. Polar Saturation (Bottom)
A polar plot where:
* **Angle:** Represents Hue.
* **Distance from Center:** Represents Saturation (Normalized to the most saturated color in the palette).
"""
        with open(OUTPUT_MD, "w") as f:
            f.write(md_content)
        print(f"Markdown saved to {OUTPUT_MD}")

if __name__ == "__main__":
    run()
