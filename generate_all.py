import os
import main
from modules import module1, module2, module3, module4, module5, module6, module7, module8, ultimate

def generate_all():
    print(f"Starting Batch Generation for {len(main.THEMES)} themes...")
    
    # Ensure base directories exist
    os.makedirs("images/themes", exist_ok=True)
    os.makedirs("images/ultimate", exist_ok=True)

    sorted_themes = sorted(main.THEMES.keys())
    
    for i, theme_name in enumerate(sorted_themes):
        print(f"\n[{i+1}/{len(sorted_themes)}] Processing Theme: {theme_name}")
        
        palette = main.THEMES[theme_name]
        scheme = main.generate_color_scheme(theme_name, palette)
        
        theme_dir_name = theme_name.replace(" ", "_")
        images_dir = os.path.join("images", "themes", theme_dir_name)
        ultimate_dir = os.path.join("images", "ultimate")
        ultimate_output = os.path.join(ultimate_dir, f"{theme_dir_name}_ultimate.png")

        # Skip if already processed
        if os.path.exists(ultimate_output):
            print(f"  >> Skipping: {theme_name} (Already exists)")
            continue

        os.makedirs(images_dir, exist_ok=True)

        modules_list = [
            ("Module 1", module1, "module1"),
            ("Module 2", module2, "module2"),
            ("Module 3", module3, "module3"),
            ("Module 4", module4, "module4"),
            ("Module 5", module5, "module5"),
            ("Module 6", module6, "module6"),
            ("Module 7", module7, "module7"),
            ("Module 8", module8, "module8"),
        ]

        for mod_name, mod, filename in modules_list:
            try:
                out_img = os.path.join(images_dir, f"{theme_dir_name}_{filename}.png")
                mod.run(scale=main.GLOBAL_SCALE, color_scheme=scheme, output_image=out_img)
            except Exception as e:
                print(f"  !! Error in {mod_name}: {e}")

        # Generate ultimate
        try:
            ultimate.run(
                scale=main.GLOBAL_SCALE, 
                color_scheme=scheme, 
                output_path=ultimate_output, 
                input_dir=images_dir, 
                prefix=theme_dir_name
            )
            print(f"  >> Success: {theme_name}")
        except Exception as e:
            print(f"  !! Error in Ultimate: {e}")

    print("\nBatch generation complete.")

if __name__ == "__main__":
    generate_all()
