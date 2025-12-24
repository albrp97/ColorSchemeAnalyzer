import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Import all modules
from modules import module1, module2, module3, module4, module5, module6, module7, module8

DEFAULT_SCALE = 1.0

def darken_color(rgb, factor=0.7):
    return tuple(max(0, int(c * factor)) for c in rgb)

def run(scale=DEFAULT_SCALE, color_scheme=None, output_path=None, input_dir=None, prefix=None):
    if not color_scheme:
        print("Error: No color scheme provided to ultimate module.")
        return

    print("Generating Ultimate Image...")
    
    # 1. Load all module images
    if input_dir:
        if prefix:
            image_paths = [
                os.path.join(input_dir, f"{prefix}_module{i}.png") for i in range(1, 9)
            ]
        else:
            image_paths = [
                os.path.join(input_dir, f"module{i}.png") for i in range(1, 9)
            ]
    else:
        image_paths = [
            os.path.join("images", f"module{i}.png") for i in range(1, 9)
        ]
    
    images = []
    for path in image_paths:
        if not os.path.exists(path):
            print(f"  Warning: {path} not found. Skipping.")
            continue
        img = Image.open(path).convert("RGBA")
        
        # 2. Intelligent Trimming
        # We want to remove the header and the bottom blank space
        # The header is usually the top part with the title
        margin = int(40 * scale)
        line_y = margin + int(40 * scale)
        spacing = int(20 * scale)
        content_y = line_y + spacing + int(20 * scale)
        
        # Crop top: keep a bit of space above the first panel titles
        crop_top = content_y - int(35 * scale)
        img = img.crop((0, max(0, crop_top), img.width, img.height))
        
        # Trim bottom blank space
        # Convert to numpy to find non-background pixels
        bg_color = color_scheme['BG_COLOR']
        img_np = np.array(img, dtype=np.int16)
        bg_rgb = np.array(bg_color, dtype=np.int16)
        
        # A pixel is "content" if it's different from the background
        # We use a very low tolerance now to avoid cropping dark UI elements
        diff_bg = np.abs(img_np[:, :, :3] - bg_rgb)
        is_bg = np.all(diff_bg < 10, axis=2)
        
        # Content is anything that is NOT background
        non_bg = ~is_bg
            
        rows = np.any(non_bg, axis=1)
        if np.any(rows):
            last_row = np.where(rows)[0][-1]
            # Add a tiny bit of padding (5px) for breathing room
            img = img.crop((0, 0, img.width, last_row + int(5 * scale)))
        
        images.append(img)

    if len(images) < 8:
        print("  Error: Not all module images were found.")
        return

    # 3. Layout Design
    # images[0]=M1, images[1]=M2, images[2]=M3, images[3]=M4
    # images[4]=M5, images[5]=M6, images[6]=M7, images[7]=M8
    
    # Balanced Columns:
    # Col 1: M1, M2, M3, M4, M6
    # Col 2: M7, M8, M5
    col1_indices = [0, 1, 2, 3, 5]
    col2_indices = [6, 7, 4]
    
    col1_width = max(images[i].width for i in col1_indices)
    col2_width = max(images[i].width for i in col2_indices)
    
    gap = int(40 * scale)
    total_width = col1_width + col2_width + (3 * gap)
    
    col1_height = sum(images[i].height for i in col1_indices) + (len(col1_indices) * gap)
    
    # 4. Prepare Title Box (Industrial Style)
    title_text = f"{color_scheme.get('THEME_NAME', 'Custom').upper()} PALETTE"
    header_label = "COLOR SCHEME ANALYZER"
    author_text = "by albrp97"
    
    try:
        font_title = ImageFont.truetype(color_scheme['FONT_FILENAME'], int(35 * scale))
        font_label = ImageFont.truetype(color_scheme['FONT_FILENAME'], int(18 * scale))
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    # Box dimensions
    box_w = int(col2_width * 0.9)
    box_h = int(100 * scale)
    title_box_total_h = box_h + int(60 * scale) # Including labels and padding
    
    col2_height = sum(images[i].height for i in col2_indices) + (len(col2_indices) * gap) + title_box_total_h
    
    # Reduce header height and tighten layout
    header_h = gap
    content_height = max(col1_height, col2_height) + header_h
    
    # 5. Add Darker Margin
    outer_margin = int(120 * scale)
    darker_bg = darken_color(color_scheme['BG_COLOR'], 0.6)
    
    total_width_final = total_width + (2 * outer_margin)
    total_height_final = content_height + (2 * outer_margin)
    
    ultimate = Image.new('RGB', (total_width_final, total_height_final), darker_bg)
    draw = ImageDraw.Draw(ultimate)
    
    # Draw the inner background rectangle
    draw.rectangle([outer_margin, outer_margin, outer_margin + total_width, outer_margin + content_height], fill=color_scheme['BG_COLOR'])
    
    # 6. Paste Images (Offset by outer_margin)
    # Column 1
    curr_y = header_h + outer_margin
    for i in col1_indices:
        img = images[i]
        x_off = outer_margin + gap + (col1_width - img.width) // 2
        ultimate.paste(img, (x_off, curr_y))
        curr_y += img.height + gap
        
    # Column 2
    curr_y = header_h + outer_margin
    for i in col2_indices:
        img = images[i]
        x_off = outer_margin + gap + col1_width + gap + (col2_width - img.width) // 2
        ultimate.paste(img, (x_off, curr_y))
        curr_y += img.height + gap

    # 7. Draw Title Box at the end of Column 2
    # Center the box in the second column
    box_x = outer_margin + gap + col1_width + gap + (col2_width - box_w) // 2
    box_y = curr_y + int(30 * scale) 
    
    # Top Label (Industrial Style)
    draw.text((box_x, box_y - int(22 * scale)), header_label, fill=color_scheme['TEXT_MAIN'], font=font_label)
    
    # Main Box
    border_width = max(1, int(1 * scale))
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], outline=color_scheme['UI_BORDER'], width=border_width)
    
    # Centered Title inside box
    t_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    t_w = t_bbox[2] - t_bbox[0]
    t_h = t_bbox[3] - t_bbox[1]
    
    # Centered Author inside box (below title)
    a_bbox = draw.textbbox((0, 0), author_text, font=font_label)
    a_w = a_bbox[2] - a_bbox[0]
    a_h = a_bbox[3] - a_bbox[1]
    
    total_text_h = t_h + a_h + int(10 * scale)
    start_y = box_y + (box_h - total_text_h) // 2
    
    draw.text((box_x + (box_w - t_w)//2, start_y), title_text, fill=color_scheme['TEXT_MAIN'], font=font_title)
    draw.text((box_x + (box_w - a_w)//2, start_y + t_h + int(15 * scale)), author_text, fill=color_scheme['ACCENT'], font=font_label)

    # 8. Save
    out_path = output_path if output_path else os.path.join("images", "ultimate_analysis.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ultimate.save(out_path)
    print(f"Ultimate image saved to {out_path}")
