from modules import module1
from modules import module2
from modules import module3
from modules import module4
from modules import module5
from modules import module6
from modules import module7
from modules import module8
from modules import ultimate
import os
import colorsys

# ==========================================
# CONFIGURATION
# ==========================================

# Select your theme here from the THEMES dictionary below
# Options: "Catppuccin", "Gruvbox", "Nord", "Everforest", "Dracula",
#          "RosePine", "TokyoNight", "Sweet", "Kanagawa
#          "BlackLotus", "Whale", "Everblush", "ShadesOfPurple",
#          "Opulo", "Camellia", "Artzen", "Eva_Unit01", "Eva_Unit00",
#          "Eva_Unit00_Proto", "Eva_Unit02", "Eva_Unit06", "Eva_Unit08",
#          "Eva_MassProd", "Matrix", "GhostInTheShell", "HankaRobotics",
#          "Akira", "BladeRunner", "BladeRunner2049", "MrRobot"
CURRENT_THEME_NAME = "Artzen" 

# Global Scale: 1.0 = Native, 0.5 = Pixelated, 2.0 = High Definition
GLOBAL_SCALE = 0.5

# Font Configuration
FONT_FILENAME = "JetBrainsMono-Regular.ttf"
FONT_URL = "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf"

# ==========================================
# THEME DEFINITIONS
# ==========================================

THEMES = {
    "Catppuccin": [ # Mocha variant
        "#1e1e2e", "#181825", "#313244", "#45475a", "#585b70", 
        "#cdd6f4", "#f5e0dc", "#b4befe", "#f38ba8", "#fab387", 
        "#f9e2af", "#a6e3a1", "#94e2d5", "#89b4fa", "#cba6f7"
    ],
    "Gruvbox": [ # Dark
        "#282828", "#3c3836", "#504945", "#665c54", "#7c6f64", 
        "#ebdbb2", "#cc241d", "#98971a", "#d79921", "#458588", 
        "#b16286", "#689d6a", "#d65d0e", "#fb4934", "#b8bb26"
    ],
    "Nord": [
        "#2E3440", "#3B4252", "#434C5E", "#4C566A",
        "#D8DEE9", "#E5E9F0", "#ECEFF4",
        "#8FBCBB", "#88C0D0", "#81A1C1", "#5E81AC",
        "#BF616A", "#D08770", "#EBCB8B", "#A3BE8C", "#B48EAD"
    ],
    "Everforest": [
        "#1E2326", "#272E33", "#2E383C", "#374145", "#414B50", "#495156", "#4F5B58",
        "#493B40", "#45443C", "#3C4841", "#384B55", "#463F48", "#4C3743", "#D3C6AA",
        "#E67E80", "#DBBC7F", "#A7C080", "#7FBBB3", "#D699B6", "#83C092", "#E69875",
        "#7A8478", "#859289", "#9DA9A0"
    ],
    "Dracula": [
        "#282a36", "#44475a", "#f8f8f2", "#6272a4", "#8be9fd", 
        "#50fa7b", "#ffb86c", "#ff79c6", "#bd93f9", "#ff5555", 
        "#f1fa8c"
    ],
    "RosePine": [
        "#232136", "#2a273f", "#393552", "#6e6a86", "#908caa", 
        "#e0def4", "#eb6f92", "#f6c177", "#ea9a97", "#3e8fb0", 
        "#9ccfd8", "#c4a7e7", "#2a283e", "#44415a", "#56526e"
    ],
    "TokyoNight": [
        "#1a1b26", "#24283b", "#414868", "#565f89", "#a9b1d6", 
        "#c0caf5", "#f7768e", "#ff9e64", "#e0af68", "#9ece6a", 
        "#73daca", "#7aa2f7", "#bb9af7"
    ],
    "Sweet": [
        "#161925", "#0c0e14", "#c3c7d1", "#ff00a0", "#a000ff", 
        "#00a0ff", "#00ff00", "#ffff00", "#ff0000", "#363a4e"
    ],
    "Kanagawa": [
        "#1F1F28", "#2A2A37", "#363646", "#DCD7BA", "#C8C093", 
        "#E46876", "#FF5D62", "#FFA066", "#E6C384", "#98BB6C", 
        "#7E9CD8", "#957FB8"
    ],
    "BlackLotus": [
        "#1c1e26", "#232530", "#5c6282", "#dcdfe4", "#e75a7c", 
        "#f1c40f", "#48dbfb", "#9b59b6", "#e056fd", "#1dd1a1"
    ],
    "Whale": [
        "#0e1319", "#151a21", "#323842", "#dfe5ed", "#e691a3", 
        "#c7a5d1", "#78b4ac", "#6ca3c7", "#acb891", "#d9bd86"
    ],
    "Everblush": [
        "#141b1e", "#232a2d", "#dadada", "#e07a5f", "#8ccf7e", 
        "#e5c76b", "#67b0e8", "#c47fd5", "#6cbfbf", "#b3b9b8"
    ],
    "ShadesOfPurple": [
        "#2D2B55", "#1E1E3F", "#A599E9", "#FAD000", "#B362FF", 
        "#9EFFFF", "#FF9D00", "#FF629E", "#5af78e"
    ],
    "Opulo": [
        "#111111", "#1c1c1c", "#333333", "#dddddd", "#ff3d5e", 
        "#3dffca", "#8e44ad", "#f1c40f", "#4a69bd", "#e55039"
    ],
    "Camellia": [
        "#0d0d14", "#181824", "#e0e0e5", "#ff476e", "#e06c75", 
        "#98c379", "#e5c07b", "#61afef", "#c678dd", "#56b6c2"
    ],
    "Artzen": [
        "#181c1f", "#181c1f", # Backgrounds
        "#fdf9f8", "#9a8c8a", # Foregrounds (Bright, Dim)
        "#bb6d6c", "#da7a6f", # Accents (Red, Orange)
        "#9f6769", "#9b584d", # Muted/Dark Reds
        "#b97670", "#d7b2ae",  # Additional tones
        "#e28e61", "#d65160"
    ],
    "Eva_Unit01": [ # Shinji: Purple, Neon Green, Black, Orange
        "#141414", "#1e1b26", "#2d2438", "#453a59", "#6d3e91", 
        "#9b59b6", "#a29bfe", "#e0e0e0", "#39ff14", "#69f0ae", 
        "#ff9f43", "#e67e22", "#d63031", "#8e44ad", "#2ecc71"
    ],
    "Eva_Unit00": [ # Rei (Blue): Cobalt Blue, White, Grey, Black
        "#1a1c23", "#232730", "#2c3e50", "#34495e", "#57606f", 
        "#95a5a6", "#bdc3c7", "#ecf0f1", "#3498db", "#2980b9", 
        "#e74c3c", "#f39c12", "#7f8c8d", "#dff9fb", "#ffffff"
    ],
    "Eva_Unit00_Proto": [ # Rei (Orange): Industrial Orange, White, Grey
        "#1e1e1e", "#252526", "#333333", "#4d4d4d", "#808080", 
        "#d1d1d1", "#ffffff", "#f1c40f", "#f39c12", "#e67e22", 
        "#d35400", "#c0392b", "#3498db", "#2ecc71", "#ecf0f1"
    ],
    "Eva_Unit02": [ # Asuka: Scarlet Red, Orange, Green (eyes), White
        "#1a0f0f", "#2b1212", "#4a1c1c", "#752222", "#a62828", 
        "#c0392b", "#e74c3c", "#ff7675", "#fab1a0", "#fdcb6e", 
        "#ffeaa7", "#55efc4", "#00b894", "#d63031", "#ffffff"
    ],
    "Eva_Unit06": [ # Kaworu: Navy, Gold, Grey, Red Visor
        "#0c1016", "#121824", "#1a2639", "#24344d", "#304766", 
        "#8da0b8", "#dbe4eb", "#f1c40f", "#f39c12", "#c0392b", 
        "#e74c3c", "#95a5a6", "#34495e", "#f3f0ff", "#ffffff"
    ],
    "Eva_Unit08": [ # Mari: Pink, White, Green
        "#1f1a1d", "#292025", "#3d2e36", "#614051", "#8a5a72", 
        "#d9aebb", "#fce4ec", "#ffffff", "#e056fd", "#ff79c6", 
        "#fd79a8", "#55efc4", "#00b894", "#fab1a0", "#ffeaa7"
    ],
    "Eva_MassProd": [ # The Series: Bone White, Dark Grey, Nightmare Red
        "#121212", "#1c1c1c", "#2d2d2d", "#595959", "#8c8c8c", 
        "#bfbfbf", "#e6e6e6", "#ffffff", "#800000", "#a80000", 
        "#c0392b", "#e74c3c", "#5c5c5c", "#7f8c8d", "#bdc3c7"
    ],
    "Matrix": [ # Digital Rain: Black, Dark Greens, Phosphor Green
        "#000000", "#020a02", "#0d1f0d", "#1a331a", "#2e4d2e", 
        "#8cbf8c", "#b3d9b3", "#e6ffe6", "#008f11", "#00ff41", 
        "#22b455", "#003b00", "#33cc33", "#80ff80", "#aaffaa"
    ],
    "GhostInTheShell": [ # 1995 Anime: Thermoptic Blue, City Grey, Wireframe Green
        "#12161a", "#1b2630", "#263645", "#384d5e", "#5c707d", 
        "#bdc3c7", "#d1d8e0", "#ecf0f1", "#00a8ff", "#0097e6", 
        "#4cd137", "#2f3640", "#7f8fa6"
    ],
    "HankaRobotics": [ # Corporate: Sterile Lab White, Surgical Steel, Logo Red
        "#0f1114", "#161b22", "#21262d", "#30363d", "#484f58", 
        "#8b949e", "#c9d1d9", "#f0f6fc", "#d73a49", "#ff7b72", 
        "#a5d6ff", "#7ee787", "#ffa657", "#f2cc60", "#ffffff"
    ],
    "Akira": [ # Neo-Tokyo: Asphalt, Kaneda Red, Energy Blue, Laser Green
        "#141414", "#1f1f1f", "#2b2b2b", "#404040", "#737373", 
        "#d9d9d9", "#ffffff", "#ff0000", "#ba0c2f", "#e62e00", 
        "#26c6da", "#42a5f5", "#66bb6a", "#ffee58", "#5c5c5c"
    ],
    "BladeRunner": [ # 1982: Noir Shadow, Sepia Smog, Neon Pink & Blue
        "#08090a", "#141619", "#22262b", "#4b453e", "#7a7266", 
        "#a8a193", "#d6d0c4", "#ffffff", "#0077be", "#2980b9", 
        "#e056fd", "#be2edd", "#eb4d4b", "#f0932b", "#95afc0"
    ],
    "BladeRunner2049": [ # Vegas Dust: Orange Haze, Brutalist Grey, Hologram Purple
        "#1a1614", "#26201c", "#3d342f", "#5e524a", "#8c7b70", 
        "#d9cfc8", "#f2f2f2", "#ff9f43", "#f39c12", "#e67e22", 
        "#0984e3", "#74b9ff", "#a29bfe", "#fd79a8", "#dfe6e9"
    ],
    "MrRobot": [ # Fsociety: Terminal Black, Daemon Red, Encryption White/Teal
        "#000000", "#0a0a0a", "#1a1a1a", "#333333", "#4d4d4d", 
        "#b3b3b3", "#e6e6e6", "#ffffff", "#b90e0a", "#e74c3c", 
        "#008080", "#20b2aa", "#40e0d0", "#7fdbff", "#f0f0f0"
    ],"Pikachu": [ # Electric Rodent: Black/Brown darks, vibrant Yellows, Red cheeks
        "#1a1712", "#2c2924", "#4a443b", "#756953", "#c7b695", 
        "#f8f2e0", "#fcd147", "#ffd700", "#e74c3c", "#c0392b", 
        "#6d4c41", "#f4e64a", "#ffffff"
    ],
    "Rainbow": [ # The Spectrum: Dark neutral background to make colors pop
        "#101010", "#1a1a1a", "#333333", "#707070", "#f0f0f0", 
        "#ffffff", "#ff0000", "#ff7f00", "#ffff00", "#00ff00", 
        "#0000ff", "#4b0082", "#9400d3", "#e64980", "#ff8787"
    ],
    "DunePart1": [ # Arrakis Day: Desert sands, spice, deep shadows, pale sky
        "#14110f", "#1f1b18", "#3b3228", "#5c5142", "#8c7b66", 
        "#d9c7a8", "#f7e7ce", "#c27843", "#e67e22", "#d35400", 
        "#a67b5b", "#8c6046", "#b08d57", "#e69b56"
    ],
    "DunePart2": [ # Giedi Prime & War: Monochrome sun, brutal reds, stark contrast
        "#0a0a0a", "#141414", "#212121", "#404040", "#808080", 
        "#d1d1d1", "#ffffff", "#7a1313", "#a61a1a", "#e74c3c", 
        "#ff2200", "#c0392b", "#f39c12", "#95a5a6"
    ],
    "Ocean": [ # The Abyss to Surface: Deep trenches, vibrant reefs, seafoam
        "#05111a", "#0a1e2b", "#132e40", "#1d435c", "#356380", 
        "#668da3", "#9ec4d9", "#e0f7fa", "#005b96", "#03396c", 
        "#0077be", "#00a8e8", "#00b894", "#55efc4", "#ff7675"
    ],
    "Galaxy": [ # Deep Space: Vantablack, nebular purples/pinks, bright starpoints
        "#030308", "#0d0d1a", "#1a1a2e", "#2b2b4a", "#454569", 
        "#c0c0d9", "#e6e6fa", "#ffffff", "#6a0dad", "#8a2be2", 
        "#ff00ff", "#e056fd", "#00ffff", "#00bfff", "#4169e1"
    ],
    "Cyberpunk2077": [ # Night City: Samurai Yellow, Glitch Blue, Dark Grid
        "#000000", "#181818", "#2a2a2a", "#fcee0a", "#00f0ff", 
        "#ff003c", "#39ff14", "#ffffff", "#b3b3b3", "#ededed", 
        "#2de2e6", "#fdfa2a", "#ff2a6d", "#05d9e8", "#d1f7ff"
    ],
    "Vaporwave": [ # 1995 Aesthetic: Greek Busts, Windows 95, Neon Pastels
        "#181226", "#251b3b", "#362657", "#ff71ce", "#01cdfe", 
        "#05ffa1", "#b967ff", "#fffb96", "#2c2c54", "#e0e0e0", 
        "#ffffff", "#ff9ff3", "#feca57", "#48dbfb", "#5f27cd"
    ],
    "Monokai": [ # The Classic: Sublime Text's legacy. High contrast & industrial
        "#272822", "#3e3d32", "#75715e", "#f8f8f2", "#66d9ef", 
        "#a6e22e", "#f92672", "#fd971f", "#e6db74", "#ae81ff", 
        "#cfcfc2", "#d6d6d6", "#ffffff", "#49483e", "#a1efe4"
    ],
    "SolarizedDark": [ # Low Contrast: Ethan Schoonover's masterpiece. Teal-based.
        "#002b36", "#073642", "#586e75", "#657b83", "#839496", 
        "#93a1a1", "#eee8d5", "#fdf6e3", "#b58900", "#cb4b16", 
        "#dc322f", "#d33682", "#6c71c4", "#268bd2", "#2aa198", "#859900"
    ],
    "SpiderVerse": [ # Miles Morales: Glitch, Ben-Day dots, Ink Black, Neon
        "#000000", "#0a0a0a", "#141414", "#202020", "#ffffff", 
        "#ff003c", "#05f2db", "#fafe35", "#a020f0", "#453a59", 
        "#e0e0e0", "#ff3333", "#00ccff", "#ccff00", "#9900cc"
    ],
    "TronLegacy": [ # The Grid: Bioluminescent Cyan, Orange, Deepest Grey
        "#0d0d0d", "#1a1a1a", "#262626", "#333333", "#ffffff", 
        "#6fc3df", "#ffe64d", "#df740c", "#e6ffff", "#8fd8f7", 
        "#00a1e4", "#d95a00", "#ffcc00", "#f2f2f2", "#808080"
    ],
    "Gameboy": [ # DMG-01: Retro Green Monochrome (Adapted for visibility)
        "#0f380f", "#306230", "#8bac0f", "#9bbc0f", "#081820", # Original 4 + Black
        "#e0f8cf", "#ffffff", "#4b5c22", "#2e4018", "#1c2b12", 
        "#d4e8b8", "#c8dcb0", "#a8c090", "#789060", "#506840"
    ],
    "Coffee": [ # Latte Art: Warm browns, creams, espresso (Relaxing)
        "#1f1a17", "#2e2520", "#42362e", "#594a40", "#736255", 
        "#8c7a6b", "#a69586", "#bfb2a6", "#d9d0c7", "#f2f0eb", 
        "#c0392b", "#d35400", "#e67e22", "#f1c40f", "#ffffff"
    ],
    "NierAutomata": [ # Glory to Mankind: Warm Dark Greys, Signature Beige, Muted Alert Red
        "#23211e", "#2b2b28", "#383530", "#48453e", "#58544a", 
        "#6b655a", "#878170", "#a39d88", "#dad4bb", "#eae5d1", 
        "#c4bd9e", "#9e8f78", "#8c3f3f", "#cd664d", "#d6a66e"
    ],
    "Blueprint": [ # Engineering: Deep blueprint blue, white lines, safety yellow
        "#0a2e52", "#0f3d6b", "#164d85", "#24609e", "#ffffff", 
        "#dbeeff", "#f0f8ff", "#f1c40f", "#f39c12", "#e74c3c", 
        "#2ecc71", "#95a5a6", "#bdc3c7", "#ecf0f1", "#00a8ff"
    ],
    "Portal": [ # Aperture Science: Sterile Grey, Weighted Cube Pink, Portals
        "#191919", "#262626", "#404040", "#808080", "#bdc3c7", 
        "#ecf0f1", "#ffffff", "#ff9a00", "#ffba49", "#00a2ff", 
        "#2196f3", "#ff6b6b", "#e74c3c", "#34495e", "#2c3e50"
    ],
    "Minecraft": [ # The Overworld: Obsidian, Dirt, Grass, Diamond, Redstone
        "#120e0e", "#1f1a17", "#2e211b", "#3b2e2a", "#594034", 
        "#75a342", "#7dbd42", "#52eed8", "#34d9c0", "#f1c40f", 
        "#d63031", "#ff0000", "#8c8c8c", "#7f8c8d", "#ffffff"
    ],
    "Joker": [ # Gotham Villain: Deep Purple, Acid Green, Blood Red, White Face
        "#1a0a1a", "#291029", "#3b173b", "#4b2e83", "#6a1b9a", 
        "#8e44ad", "#f5f5f5", "#2ecc71", "#00ff00", "#c0392b", 
        "#e74c3c", "#f1c40f", "#ffffff", "#bdc3c7", "#2c3e50"
    ],
    "SilentHill": [ # Otherworld: Rust, Dried Blood, Fog Grey, Static Black
        "#1a1212", "#2b1d1d", "#3e2727", "#5c3a3a", "#8c3f3f", 
        "#a62828", "#bdc3c7", "#d1d8e0", "#95a5a6", "#7f8c8d", 
        "#5c5c5c", "#3d3d3d", "#dcdde1", "#c0392b", "#701616"
    ],
    "TerminalAmber": [ # CRT Monitor: Pitch black, phosphorescent amber
        "#000000", "#0a0800", "#141000", "#1f1800", "#2b2100", 
        "#ffb000", "#ffcc00", "#ffd700", "#ffaa00", "#e69500", 
        "#b37400", "#805300", "#4d3200", "#ffffff", "#f1f1f1"
    ],
    "Starfield": [ # NASA-Punk: Void Black, Ship White, Constellation Ribbon (Red/Orange/Gold/Blue)
        "#0b0d12", "#151921", "#232a35", "#3d4756", "#5a6575", 
        "#dce1e6", "#ffffff", "#cf4639", "#de8e36", "#d4af37", 
        "#2c5282", "#3a7cbd", "#4fd1c5", "#8195a8", "#1a1a1a"
    ],

}

# ==========================================
# INTERFACE
# ==========================================

def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    # Handle short hex (e.g. #fff) just in case
    if len(h) == 3:
        h = ''.join([c*2 for c in h])
    # Handle alpha channel (RGBA) by stripping it for analysis purposes
    if len(h) == 8:
        h = h[:6]
        
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def select_theme_terminal(themes):
    """
    Creates a terminal-based interface to select a theme with color previews.
    """
    print("\n" + "="*50)
    print(" SELECT COLOR SCHEME")
    print("="*50 + "\n")
    
    sorted_names = sorted(themes.keys())
    
    for i, name in enumerate(sorted_names):
        colors = themes[name]
        # Create a small color strip using ANSI escape codes
        color_strip = ""
        for hex_color in colors[:10]: # Show first 10 colors
            r, g, b = hex_to_rgb(hex_color)
            # ANSI background color: \033[48;2;R;G;Bm  \033[0m
            color_strip += f"\033[48;2;{r};{g};{b}m  \033[0m"
        
        print(f"[{i+1:2}] {name:20} {color_strip}")
    
    print("\n" + "="*50)
    try:
        choice = input(f"\nSelect a theme (1-{len(sorted_names)}) or press Enter for default: ").strip()
        if not choice:
            return None
        
        idx = int(choice) - 1
        if 0 <= idx < len(sorted_names):
            return sorted_names[idx]
    except (ValueError, IndexError, KeyboardInterrupt):
        pass
    
    return None

# ==========================================
# CORE LOGIC
# ==========================================

def get_luminance(rgb): 
    return 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]

def get_saturation(rgb):
    r, g, b = [x/255.0 for x in rgb]
    try:
        _, s, _ = colorsys.rgb_to_hsv(r, g, b)
        return s
    except:
        return 0

def generate_color_scheme(theme_name, palette_hex):
    print(f"Applying Theme: {theme_name}")
    
    _rgb_palette = [hex_to_rgb(c) for c in palette_hex]
    
    # Sort for algorithmic assignment
    _sorted_by_lum = sorted(_rgb_palette, key=get_luminance)
    _sorted_by_sat = sorted(_rgb_palette, key=get_saturation)

    # Dynamic assignment logic based on list length
    bg_idx = 0
    ui_border_idx = min(3, len(_sorted_by_lum)-1)
    text_main_idx = -1
    text_dim_idx = min(3, len(_sorted_by_lum)-1)
    if len(_sorted_by_lum) > 4: 
        # If palette is large enough, ensure dim text is brighter than border
        text_dim_idx = len(_sorted_by_lum) // 2 

    return {
        "PALETTE_HEX": palette_hex,
        "BG_COLOR": _sorted_by_lum[bg_idx],
        "UI_BORDER": _sorted_by_lum[ui_border_idx],
        "TEXT_MAIN": _sorted_by_lum[text_main_idx],
        "TEXT_DIM": _sorted_by_lum[text_dim_idx],
        "ACCENT": _sorted_by_sat[-1], # Most saturated color
        "PLOT_BG": _sorted_by_lum[min(1, len(_sorted_by_lum)-1)],
        "GRID_LINE": _sorted_by_lum[min(1, len(_sorted_by_lum)-1)],
        "FONT_FILENAME": FONT_FILENAME,
        "FONT_URL": FONT_URL,
        "THEME_NAME": theme_name
    }

def main():
    # Launch the terminal theme selector
    selected = select_theme_terminal(THEMES)
    if selected:
        active_name = selected
        active_palette = THEMES[selected]
    else:
        # If no selection made, use the default from config
        print(f"Using default theme: {CURRENT_THEME_NAME}")
        active_name = CURRENT_THEME_NAME
        active_palette = THEMES.get(active_name, THEMES["Nord"])

    # Generate the scheme object
    scheme = generate_color_scheme(active_name, active_palette)

    # Define output paths
    theme_dir = active_name.replace(" ", "_")
    images_dir = os.path.join("images", "themes", theme_dir)
    ultimate_dir = os.path.join("images", "ultimate")
    
    ultimate_output = os.path.join(ultimate_dir, f"{theme_dir}_ultimate.png")

    # Check if already processed
    if os.path.exists(ultimate_output):
        print(f"\nTheme '{active_name}' already processed. Skipping analysis.")
        print(f"Ultimate image: {ultimate_output}")
        return

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(ultimate_dir, exist_ok=True)

    print(f"Starting Color Study Analysis Suite [Scale: {GLOBAL_SCALE}]...")
    
    modules_list = [
        ("Module 1: Industrial Color Study", module1, "module1"),
        ("Module 2: Aligned Linear Analysis", module2, "module2"),
        ("Module 3: 3D Space & Distribution", module3, "module3"),
        ("Module 4: The Master Strip", module4, "module4"),
        ("Module 5: 4x4 Matrix & Normalized Polar Analysis", module5, "module5"),
        ("Module 6: Hybrid Gamut", module6, "module6"),
        ("Module 7: Complementary Desaturation Planes", module7, "module7"),
        ("Module 8: Primary Ranges", module8, "module8"),
    ]
    
    for name, mod, filename in modules_list:
        print(f"\nExecuting {name}...")
        try:
            # Pass the generated scheme and output paths to the module
            out_img = os.path.join(images_dir, f"{theme_dir}_{filename}.png")
            mod.run(scale=GLOBAL_SCALE, color_scheme=scheme, output_image=out_img)
        except Exception as e:
            print(f"Error executing {name}: {e}")
            
    # Generate the ultimate combined image
    try:
        ultimate.run(scale=GLOBAL_SCALE, color_scheme=scheme, output_path=ultimate_output, input_dir=images_dir, prefix=theme_dir)
    except Exception as e:
        print(f"Error generating ultimate image: {e}")

    print("\nAll modules executed successfully.")
    print(f"Images: {images_dir}")
    print(f"Ultimate: {ultimate_output}")

if __name__ == "__main__":
    main()