import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import os
import urllib.request
import math

# ==========================================
# CONFIGURATION
# ==========================================
DEFAULT_SCALE = 1.0
OUTPUT_IMAGE = os.path.join("images", "module3.png")

# Configuration inherited from main.py
PALETTE_HEX = []
BG_COLOR = (0, 0, 0)
UI_BORDER = (0, 0, 0)
TEXT_MAIN = (0, 0, 0)
TEXT_DIM = (0, 0, 0)
ACCENT = (0, 0, 0)
GRID_LINE = (0, 0, 0)
FONT_FILENAME = ""
FONT_URL = ""

def run(scale=DEFAULT_SCALE, color_scheme=None, output_image=None):
    if color_scheme:
        global PALETTE_HEX, BG_COLOR, UI_BORDER, TEXT_MAIN, TEXT_DIM, ACCENT, GRID_LINE, FONT_FILENAME, FONT_URL
        PALETTE_HEX = color_scheme['PALETTE_HEX']
        BG_COLOR = color_scheme['BG_COLOR']
        UI_BORDER = color_scheme['UI_BORDER']
        TEXT_MAIN = color_scheme['TEXT_MAIN']
        TEXT_DIM = color_scheme['TEXT_DIM']
        ACCENT = color_scheme['ACCENT']
        GRID_LINE = color_scheme['GRID_LINE']
        FONT_FILENAME = color_scheme['FONT_FILENAME']
        FONT_URL = color_scheme['FONT_URL']

    out_img = output_image if output_image else OUTPUT_IMAGE

    os.makedirs(os.path.dirname(out_img), exist_ok=True)
    study = ThreeDAnalysisFinalV3(PALETTE_HEX)
    img = study.assemble(scale)
    img.save(out_img)
    print(f"Saved {out_img}")

# Layout Config (Base dimensions at scale 1.0)
BASE_WIDTH = 1600
BASE_HEIGHT = 800
BASE_MARGIN = 40
BASE_SPACING = 20

class ThreeDAnalysisFinalV3:
    def __init__(self, palette_hex):
        self.palette_hex = palette_hex
        self.rgb_colors = np.array([self.hex_to_rgb_norm(c) for c in palette_hex])
        self.luminance = np.array([0.299*r + 0.587*g + 0.114*b for r,g,b in self.rgb_colors])
        self.hsv_colors = np.array([colorsys.rgb_to_hsv(*c) for c in self.rgb_colors])

    def hex_to_rgb_norm(self, hex_str):
        h = hex_str.lstrip('#')
        return [int(h[i:i+2], 16)/255.0 for i in (0, 2, 4)]

    def load_fonts(self, scale):
        if not os.path.exists(FONT_FILENAME):
            try: urllib.request.urlretrieve(FONT_URL, FONT_FILENAME)
            except: pass
        
        size_label = int(max(6, 12 * scale))
        size_header = int(max(10, 24 * scale))
        size_tiny = int(max(5, 10 * scale))
        
        try:
            self.font_label = ImageFont.truetype(FONT_FILENAME, size_label)
            self.font_header = ImageFont.truetype(FONT_FILENAME, size_header)
            self.font_tiny = ImageFont.truetype(FONT_FILENAME, size_tiny)
        except:
            self.font_label = ImageFont.load_default()
            self.font_header = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

    def draw_ui_element(self, draw, x, y, w, h, title, subtitle, scale):
        text_padding = int(5 * scale)
        title_y = y - int(22 * scale) 
        draw.text((x, title_y), title, fill=TEXT_MAIN, font=self.font_label)
        
        sub_bbox = draw.textbbox((0, 0), subtitle, font=self.font_tiny)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_y = y + h + text_padding
        draw.text((x + w - sub_w, sub_y), subtitle, fill=TEXT_DIM, font=self.font_tiny)
        
        border_width = max(1, int(1 * scale))
        draw.rectangle([x-1, y-1, x+w, y+h], outline=UI_BORDER, width=border_width)

    def render_organic_bri_match(self, w, h, scale):
        img = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        scale_w = int(w * 0.25)
        scale_img = Image.new('RGB', (scale_w, h))
        scale_draw = ImageDraw.Draw(scale_img)
        
        for y in range(h):
            val = int(255 - (y / h) * 205) 
            scale_draw.line([(0, y), (scale_w, y)], fill=(val, val, val))
        img.paste(scale_img, (0, 0))
        
        stack_x = scale_w
        stack_w = w - scale_w
        sorted_indices = np.argsort(self.luminance)
        n = len(sorted_indices)
        avg_h = h / n
        prev_boundary_y = np.zeros(stack_w)
        
        for i in range(n):
            idx = sorted_indices[i]
            col = self.rgb_colors[idx]
            rgb = tuple(int(c*255) for c in col)
            target_y = (i + 1) * avg_h
            curr_boundary_y = np.zeros(stack_w)
            
            if i == n - 1:
                curr_boundary_y[:] = h
            else:
                phase = i * 2.5
                freq = 0.05
                amp = int(10 * scale)
                for x in range(stack_w):
                    wave = math.sin(x * freq + phase) * amp
                    wave2 = math.cos(x * freq * 2.3 + phase) * (amp * 0.3)
                    y_val = target_y + wave + wave2
                    curr_boundary_y[x] = min(h, max(0, y_val))
            
            for x in range(stack_w):
                y_start = int(prev_boundary_y[x])
                y_end = int(curr_boundary_y[x])
                if y_end > y_start:
                    draw.rectangle([stack_x + x, y_start, stack_x + x, y_end], fill=rgb)
            prev_boundary_y = curr_boundary_y

        for i in range(1, 5):
            y_tick = int(i * (h / 5))
            draw.line([scale_w - int(5*scale), y_tick, scale_w, y_tick], fill=BG_COLOR, width=max(1, int(1*scale)))
        return img

    def render_iso_cube(self, w, h, scale_val, axis_order=(0, 1, 2)):
        img = Image.new('RGBA', (w, h), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        center_x, center_y = w // 2, h // 2
        padding = 10 * scale_val
        avail_w = w - (2 * padding)
        avail_h = h - (2 * padding)
        cube_scale = min(avail_w / 1.732, avail_h / 2.0)

        def to_iso(v0, v1, v2):
            angle = math.radians(30)
            ix = (v0 - v2) * math.cos(angle)
            iy = (v0 + v2) * math.sin(angle) - v1
            return center_x + ix * cube_scale, center_y - iy * cube_scale

        corners = [(0,0,0), (1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1), (1,1,1)]
        iso_corners = [to_iso(c[0], c[1], c[2]) for c in corners]
        edges = [(0,1), (0,2), (0,3), (1,4), (1,5), (2,4), (2,6), (3,5), (3,6), (4,7), (5,7), (6,7)]
        for s, e in edges:
            draw.line([iso_corners[s], iso_corners[e]], fill=GRID_LINE, width=max(1, int(1*scale_val)))
            
        colors = ["#BF616A", "#A3BE8C", "#5E81AC"]
        ox, oy = iso_corners[0]
        draw.line([ox, oy, to_iso(1.1,0,0)[0], to_iso(1.1,0,0)[1]], fill=colors[axis_order[0]], width=max(2, int(2*scale_val)))
        draw.line([ox, oy, to_iso(0,1.1,0)[0], to_iso(0,1.1,0)[1]], fill=colors[axis_order[1]], width=max(2, int(2*scale_val)))
        draw.line([ox, oy, to_iso(0,0,1.1)[0], to_iso(0,0,1.1)[1]], fill=colors[axis_order[2]], width=max(2, int(2*scale_val)))

        dot_size = int(18 * scale_val)
        for col in self.rgb_colors:
            v0, v1, v2 = col[axis_order[0]], col[axis_order[1]], col[axis_order[2]]
            ix, iy = to_iso(v0, v1, v2)
            draw.ellipse([ix-dot_size/2, iy-dot_size/2, ix+dot_size/2, iy+dot_size/2], 
                         fill=tuple(int(c*255) for c in col), outline=BG_COLOR)
        return img

    def render_grid_fill(self, w, h):
        img = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        rows, cols = 6, 6
        cw, ch = w / cols, h / rows
        palette_len = len(self.rgb_colors)
        for r in range(rows):
            for c in range(cols):
                idx = (r * cols + c) % palette_len
                col = self.rgb_colors[idx]
                x0, y0 = c * cw, r * ch
                draw.rectangle([x0, y0, x0+cw, y0+ch], fill=tuple(int(x*255) for x in col), outline=BG_COLOR)
        return img

    def render_scatter_main(self, w, h, scale):
        img = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        pad = int(20 * scale)
        plot_w, plot_h = w - 2*pad, h - 2*pad
        for i in range(5):
            pos = pad + (i/4) * plot_w
            draw.line([pos, pad, pos, h-pad], fill=GRID_LINE)
            pos_y = pad + (i/4) * plot_h
            draw.line([pad, pos_y, w-pad, pos_y], fill=GRID_LINE)
        dot_size = int(22 * scale)
        for i, col in enumerate(self.rgb_colors):
            hue = self.hsv_colors[i][0]
            bri = self.luminance[i]
            x = pad + hue * plot_w
            y = h - (pad + bri * plot_h)
            draw.ellipse([x-dot_size/2, y-dot_size/2, x+dot_size/2, y+dot_size/2], 
                         fill=tuple(int(c*255) for c in col), outline=BG_COLOR)
        return img

    def render_vertical_scatter(self, w, h, scale, data_mode="sat", invert=False):
        img = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        values = [col[1] if data_mode == "sat" else col[2] for col in self.hsv_colors]
        min_v, max_v = min(values), max(values)
        range_v = max_v - min_v if (max_v - min_v) > 0 else 1.0
        center_x = w // 2
        draw.line([center_x, 0, center_x, h], fill=GRID_LINE)
        dot_size = int(14 * scale)
        draw_h = h - dot_size
        for i, col in enumerate(self.rgb_colors):
            normalized_val = (values[i] - min_v) / range_v
            y = (dot_size // 2) + (normalized_val * draw_h) if invert else (h - (dot_size // 2)) - (normalized_val * draw_h)
            jitter = (i % 3 - 1) * int(4 * scale)
            x = center_x + jitter
            draw.ellipse([x-dot_size/2, y-dot_size/2, x+dot_size/2, y+dot_size/2], fill=tuple(int(c*255) for c in col))
        return img

    def render_shifted_bars_organized(self, w, h, scale):
        img = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        window_center_x = w // 2
        sorted_indices = np.argsort(self.luminance)
        n_bars = len(sorted_indices)
        bar_h = h / n_bars
        max_bar_width, min_bar_width = w * 0.9, int(20 * scale) 
        gap_size = int(4 * scale) 
        for i, idx in enumerate(sorted_indices):
            col, sat = self.rgb_colors[idx], self.hsv_colors[idx][1]
            total_bar_w = min_bar_width + (sat * (max_bar_width - min_bar_width))
            wave_shift = math.sin((i / n_bars) * math.pi * 2) 
            bar_center_x = window_center_x + wave_shift * (w - total_bar_w) / 2 * 0.8
            y0, y1 = int(i * bar_h), int((i+1) * bar_h)
            draw.rectangle([bar_center_x - total_bar_w/2, y0, bar_center_x - gap_size/2, y1], fill=tuple(int(c*255) for c in col))
            draw.rectangle([bar_center_x + gap_size/2, y0, bar_center_x + total_bar_w/2, y1], fill=tuple(int(c*255) for c in col))
        return img

    def assemble(self, scale=DEFAULT_SCALE):
        self.load_fonts(scale)
        w, h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
        margin, spacing = int(BASE_MARGIN * scale), int(BASE_SPACING * scale)
        canvas = Image.new('RGB', (w, h), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        draw.text((margin, margin), "3D SPACE & DISTRIBUTION // NORD_FINAL_V6", fill=TEXT_MAIN, font=self.font_header)
        line_y = margin + int(40 * scale)
        draw.line([(margin, line_y), (w - margin, line_y)], fill=UI_BORDER, width=max(1, int(2*scale)))
        content_y = line_y + spacing + int(20 * scale)
        available_h = h - content_y - margin
        col_bri_w = int(120 * scale) 
        bri_match = self.render_organic_bri_match(col_bri_w, available_h, scale)
        canvas.paste(bri_match, (margin, content_y))
        self.draw_ui_element(draw, margin, content_y, col_bri_w, available_h, "BRI MATCH", "ID:12", scale)
        rest_x = margin + col_bri_w + spacing
        col_right_w = int(250 * scale)
        col_right_x = w - margin - col_right_w
        col_mid_w = col_right_x - rest_x - spacing
        row_top_h = int(available_h * 0.4)
        row_bot_h = available_h - row_top_h - spacing
        cube_w = (col_mid_w - (2 * spacing)) // 3
        for i, order in enumerate([(0,1,2), (1,2,0), (2,0,1)]):
            cx = rest_x + i * (cube_w + spacing)
            cube = self.render_iso_cube(cube_w, row_top_h, scale, axis_order=order)
            canvas.paste(cube, (cx, content_y), cube)
            self.draw_ui_element(draw, cx, content_y, cube_w, row_top_h, f"ISO-{'ABC'[i]}", f"ID:{13+i}", scale)
        grid = self.render_grid_fill(col_right_w, row_top_h)
        canvas.paste(grid, (col_right_x, content_y))
        self.draw_ui_element(draw, col_right_x, content_y, col_right_w, row_top_h, "USEFUL HUES", "ID:16", scale)
        bot_y = content_y + row_top_h + spacing + int(20 * scale)
        row_bot_h -= int(20 * scale)
        sat_w = int(60 * scale)
        scatter_w = col_mid_w - (2 * sat_w) - (2 * spacing)
        canvas.paste(self.render_vertical_scatter(sat_w, row_bot_h, scale, "sat", False), (rest_x, bot_y))
        self.draw_ui_element(draw, rest_x, bot_y, sat_w, row_bot_h, "SAT ^", "ID:17", scale)
        scat_x = rest_x + sat_w + spacing
        canvas.paste(self.render_scatter_main(scatter_w, row_bot_h, scale), (scat_x, bot_y))
        self.draw_ui_element(draw, scat_x, bot_y, scatter_w, row_bot_h, "BRI-HUE SCATTER", "ID:18", scale)
        sat_r_x = scat_x + scatter_w + spacing
        canvas.paste(self.render_vertical_scatter(sat_w, row_bot_h, scale, "sat", True), (sat_r_x, bot_y))
        self.draw_ui_element(draw, sat_r_x, bot_y, sat_w, row_bot_h, "SAT v", "ID:19", scale)
        canvas.paste(self.render_shifted_bars_organized(col_right_w, row_bot_h, scale), (col_right_x, bot_y))
        self.draw_ui_element(draw, col_right_x, bot_y, col_right_w, row_bot_h, "BRI & SAT/WAVE", "ID:20", scale)
        return canvas

if __name__ == "__main__":
    run()
