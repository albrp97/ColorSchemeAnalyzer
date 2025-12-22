from modules import module1
from modules import module2
from modules import module3
from modules import module4
from modules import module5
from modules import module6
from modules import module7
from modules import module8
import os

# Global Scale: 1.0 = Native, 0.5 = Pixelated, 2.0 = High Definition
GLOBAL_SCALE = 0.5

def main():
    print(f"Starting Color Study Analysis Suite [Scale: {GLOBAL_SCALE}]...")
    
    modules = [
        ("Module 1: Industrial Color Study", module1),
        ("Module 2: Aligned Linear Analysis", module2),
        ("Module 3: 3D Space & Distribution", module3),
        ("Module 4: The Master Strip", module4),
        ("Module 5: 4x4 Matrix & Normalized Polar Analysis", module5),
        ("Module 6: Hybrid Gamut", module6),
        ("Module 7: Complementary Desaturation Planes", module7),
        ("Module 8: Primary Ranges", module8),
    ]
    
    for name, mod in modules:
        print(f"\nExecuting {name}...")
        try:
            mod.run(scale=GLOBAL_SCALE)
        except Exception as e:
            print(f"Error executing {name}: {e}")
            
    print("\nAll modules executed successfully.")
    print("Images: ./images/")
    print("Reports: ./reports/")
    print("Scripts: ./modules/")

if __name__ == "__main__":
    main()
