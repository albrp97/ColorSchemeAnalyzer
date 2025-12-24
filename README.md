# ColorSchemeAnalyzer

A sophisticated automated color study analysis suite that generates detailed visual reports and technical breakdowns for various color palettes.

## 🚀 Features

- **Interactive Theme Selection**: Choose from a wide variety of pre-defined themes (Catppuccin, Gruvbox, Nord, Dracula, Cyberpunk-inspired themes, and more) via a terminal-based ASCII interface.
- **Multi-Module Analysis**: 8 specialized modules analyzing different aspects of color theory:
  - **Module 1**: Industrial Color Study (Voronoi saturation models).
  - **Module 2**: Aligned Linear Analysis (Luma ramps and close matches).
  - **Module 3**: 3D Space & Distribution.
  - **Module 4**: The Master Strip.
  - **Module 5**: 4x4 Matrix & Normalized Polar Analysis.
  - **Module 6**: Hybrid Gamut.
  - **Module 7**: Complementary Desaturation Planes.
  - **Module 8**: Primary Ranges.
- **Ultimate Analysis**: Generates a combined "Master Report" image that synthesizes all module outputs into a single industrial-style infographic.
- **Smart Caching**: Automatically skips processing if a theme has already been analyzed.
- **Organized Output**: Results are neatly categorized by theme in `images/themes/` and `reports/themes/`.

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/albrp97/ColorSchemeAnalyzer.git
   cd ColorSchemeAnalyzer
   ```

2. **Install dependencies**:
   The project requires Python 3 and the Pillow (PIL) and NumPy libraries.
   ```bash
   pip install Pillow numpy
   ```

3. **Fonts**:
   The suite uses `JetBrains Mono` by default. It will attempt to download it if not present, or you can place the `.ttf` file in the root directory.

## 📖 Usage

Simply run the main script. An interactive terminal interface will appear, allowing you to select any theme from the list using your keyboard. You do **not** need to edit any files to change the theme.

```bash
python3 main.py
```

### Batch Generation

If you want to generate analysis for **all** available themes at once, use the batch script:

```bash
python3 generate_all.py
```

This script will iterate through every theme in the library, skipping those that have already been processed.

### Configuration (Optional)

While not required for theme selection, you can adjust global settings in `main.py`:
- `GLOBAL_SCALE`: Adjust output resolution (0.5 for fast previews, 2.0 for high definition).
- `CURRENT_THEME_NAME`: Set the default theme used if you simply press Enter without selecting a number.

## 📂 Project Structure

- `main.py`: Entry point and theme definitions.
- `modules/`: Individual analysis scripts.
- `images/`:
  - `themes/`: Individual module outputs organized by theme.
  - `ultimate/`: Combined master analysis images.

## 🎨 Available Themes

Includes a vast collection of themes such as:
- **Classic**: Nord, Gruvbox, Everforest, Dracula.
- **Modern**: Catppuccin, RosePine, TokyoNight, Kanagawa.
- **Cinematic**: Matrix, Blade Runner, Akira, Ghost in the Shell.
- **Special**: Eva Units (00, 01, 02, etc.), Hanka Robotics, Mr. Robot.

---
Developed by **albrp97**

# 🔬 Technical Analysis Report

This section provides a detailed breakdown of the mathematical and theoretical models used by each module in the suite.

## Module 1: Aligned Linear Analysis
**System Identifier:** `NORD_MOD1_LINEAR`
**Class:** `IndustrialColorStudy`

### 1. Executive Summary
This module performs a **Gamut Coverage Analysis** and a **Luminance Monotonicity Check**. It creates a visual stress-test of the provided palette by mapping it against a synthetic gradient field. 

The output visualizes how the discrete palette adapts to continuous lighting environments (Hue vs. Value) at fixed saturation intervals. It uses Euclidean distance in 3D RGB space to determine the "gravitational pull" or dominance of specific colors within the palette.

### 2. Submodule Breakdown

#### A. Linear Luminance Sort (Vertical Bars)
* **Identifier:** `ID:00` - `ID:03`
* **Technical Operation:** The engine decomposes the RGB vectors and calculates relative luminance using the standard Rec. 601 coefficients:
  $$Y = 0.299R + 0.587G + 0.114B$$
* **Visual Representations:**
    * **RAW:** Input array integrity check.
    * **LUM (Grayscale):** Verifies the perceived brightness curve. Used to detect "luminance collisions" (where two distinct colors share identical brightness, reducing UI contrast).
    * **REF (Sorted):** Reorders the palette by $Y$ to visualize the dynamic range from absolute black to white points.
    * **SAT+ (Maximized):** Projects colors to the surface of the HSV cylinder ($S=1.0$) to reveal the underlying hue bias without the dampening effect of low saturation.

---

## Module 2: Aligned Linear Analysis (Final)

### 1. Executive Summary
This module focuses on **chromatic integrity across variable environments** and **differential contrast**. Unlike Module 1, which analyzed spatial dominance, Module 2 stress-tests the palette's stability when specific color model components (Value, Saturation, Lightness) are clamped to fixed constants.

Additionally, it analyzes the palette's capacity for **continuous interpolation** (gradients) and identifies "collision clusters"—pairs of colors that are mathematically distinct but perceptually redundant due to low luminance delta ($\Delta L$).

### 2. Submodule Breakdown

#### A. Environmental Filter Stack
* **Identifier:** `ID:04`
* **Technical Operation:** This stack transforms the palette into four distinct color spaces to test specific component stability:
    1.  **b65% (Value Clamp):** Converts to HSV, sets $V=0.65$. Tests visibility on medium-dark UI backgrounds.
    2.  **b10% (Value Clamp):** Converts to HSV, sets $V=0.10$. Tests visibility in "Dark Mode" shadows.
    3.  **S50 (Saturation Clamp):** Converts to HSV, sets $S=0.50$. Normalizes chromatic intensity.
    4.  **L50 (Lightness Clamp):** Converts to **HLS**, sets $L=0.50$.
    
    *Note: The distinction between `b65` (HSV Value) and `l50` (HLS Lightness) is critical. HSV Value prevents color washing out to white, whereas HLS Lightness forces colors toward a "middle grey" perceptual tier.*

#### B. Linear Interpolation & Sorting
* **Identifiers:** `ID:05` - `ID:08`
* **Technical Operation:**
    * **Discrete Sorting (`ID:06`):** Reorders vectors by scalar luminance $Y$.
    * **Continuous Interpolation (`ID:07`, `ID:08`):** Generates a synthetic gradient field. For a width $w$, the pixel color at position $x$ is calculated via linear interpolation ($lerp$) between the two nearest palette indices $c_1$ and $c_2$:
      $$C_{final} = (1 - t) \cdot C_1 + t \cdot C_2$$
      Where $t$ is the fractional distance between indices.
* **Usage:**
    * **Hue Ramp (`ID:07`):** Analyzes the aesthetic smoothness of rainbow/spectrum gradients.
    * **Luma Ramp (`ID:08`):** Checks for banding artifacts in monochromatic transitions.

#### C. Differential Luminance Analysis (Match Grids)
* **Identifiers:** `ID:10 (Tight)`, `ID:11 (Loose)`
* **Technical Operation:** The module performs an $O(n^2)$ comparison of all unique palette pairs $(c_i, c_j)$. A pair is flagged and rendered if the absolute difference in luminance falls below a threshold $\epsilon$:
    $$|Y(c_i) - Y(c_j)| \le \epsilon$$
    * **$\epsilon = 0.10$ (Tight):** Colors are virtually indistinguishable in varying lighting.
    * **$\epsilon = 0.30$ (Loose):** Colors are distinct but may lack sufficient contrast for text-on-background usage.
* **Information Yield:**
    * **Redundancy Detection:** If many pairs appear in `ID:10`, the palette is "overcrowded" with similar tones, wasting token space.
    * **Accessibility Warning:** Any pair appearing here should **never** be used as a foreground/background combination (e.g., text on a button), as they fail WCAG contrast ratio standards.

### 3. Usage & Inference
**Primary Use:** Design System Optimization & Accessibility Auditing.

* **Token Rationalization:** Use the **4x4 Grid (`ID:09`)** combined with **Close Matches (`ID:10`)** to prune the palette. If two colors appear in the 10% match grid, consider merging them into a single design token to reduce system complexity.
* **Gradient Feasibility:** Inspect `ID:07`. If the gradient appears "muddy" (brownish transitions), it indicates that the interpolation through RGB space cuts through a desaturated region.
    
    *Technical Note: This linear RGB interpolation often causes "gray dead zones" compared to perceptual interpolation (like Oklab), which this module helps visualize.*

---

## Module 3: 3D Space & Distribution

### 1. Executive Summary
This module maps the palette into three-dimensional Euclidean space ($\mathbb{R}^3$) and two-dimensional planar space to analyze **gamut volume** and **clustering**. While previous modules analyzed colors in isolation or pairs, this module treats the palette as a point cloud.

It identifies whether the color scheme creates a cohesive "solid" within the RGB cube or if it exists as disjointed clusters (which can result in a fragmented user experience). It also introduces "organic" visualization techniques to simulate how colors interact when layered in complex, non-linear interfaces.

### 2. Submodule Breakdown

#### A. Volumetric Isometric Projections (The Cubes)
* **Identifiers:** `ID:13 (ISO-A)`, `ID:14 (ISO-B)`, `ID:15 (ISO-C)`
* **Technical Operation:**
  The module maps each color $C(r,g,b)$ to a 2D isometric plane using rotational transformation matrices. The projection logic used corresponds to a $30^{\circ}$ viewing angle:
  $$x' = (r - b) \cdot \cos(30^{\circ})$$
  $$y' = (r + b) \cdot \sin(30^{\circ}) - g$$
  
  * **ISO-A/B/C:** The three variations represent 90° rotations of the axis order (RGB $\to$ GBR $\to$ BRG).
* **Analysis:**
    * **Centroid Bias:** If all dots cluster in the center, the palette is "muddy" (low saturation, mid-tone).
    * **Corner Reach:** Checks if the palette reaches the "extremes" of the color engine (Cyan, Magenta, Yellow, pure Black/White). A vibrant UI palette should have points near the cube's vertices.

#### B. Planar Scatter (Hue vs. Luminance)
* **Identifier:** `ID:18 (BRI-HUE SCATTER)`
* **Technical Operation:**
  This is a Cartesian plot where:
  * $X = \text{Hue } (0^{\circ} \to 360^{\circ})$
  * $Y = \text{Luminance } (0 \to 1)$
* **Information Yield:**
  This is the primary diagnostic tool for **"Holes"**. In a robust design system, you typically want a wave-like distribution—yellows should be high $Y$, blues/purples low $Y$. If you see a cluster of high-brightness Blue, it indicates unnatural or "neon" colors that may be hard to read on white backgrounds.

#### C. 1D Distribution Vectors
* **Identifiers:** `ID:17 (SAT ^)`, `ID:19 (SAT v)`
* **Technical Operation:**
  Collapses the 3D data onto a single vertical axis based purely on **Saturation**.
  * `SAT ^`: Normal orientation (0 at bottom, 1 at top).
  * `SAT v`: Inverted.
* **Usage:** Detects "Saturation Banding". If dots are grouped tightly (e.g., everyone is at 60-70% saturation), the palette is mathematically consistent but might feel monotonous.

### 3. Organic & Harmonic Visualization

#### A. Luminance Sedimentation
* **Identifier:** `ID:12 (BRI MATCH)`
* **Technical Operation:**
  Colors are stacked by Luminance, but the boundaries are modulated by a trigonometric function:
  $$y(x) = Y_{base} + A \cdot \sin(\omega x + \phi) + A_{2} \cdot \cos(2.3\omega x)$$
* **Purpose:**
  This simulates "organic interfaces" (gradients, fluid backgrounds). It reveals if adjacent luminance tiers clash when placed in non-rectilinear shapes. If the wavy boundary between two colors vibrates visually, they cause **chromostereopsis** (depth illusion/eye strain) and should not be layered.

#### B. Harmonic Width Modulation
* **Identifier:** `ID:20 (BRI & SAT/WAVE)`
* **Technical Operation:**
  * **Y-Position:** Sorted by Luminance.
  * **Bar Width:** Proportional to Saturation ($W \propto S$).
  * **X-Offset:** Modulated by index-based Sine wave.
* **Interpretation:**
  This correlates **Impact (Saturation)** with **Hierarchy (Brightness)**.
  * **Heavy Bottom:** If the wide bars are at the bottom, the dark colors are the most saturated (typical for "Dark Mode" themes).
  * **Heavy Top:** If wide bars are at the top, the light colors are saturated (typical for "Pastel/Candy" themes).

---

## Module 4: The Master Strip

### 1. Executive Summary
This module focuses on **procedural lighting ramps** and **optical mixing**. It tests how the palette behaves when subjected to artificial lighting conditions and how colors interact when dithered together.

### 2. Submodule Breakdown

#### A. Procedural Lighting Ramps
* **Identifier:** `ID:23`
* **Technical Operation:**
  This breaks the flat color model. For every palette token $C$, it procedurally generates a 4-step lighting ramp:
  1.  **Specular (Highlight):** $C_{spec} = (C + 255) / 2$ (Tint 50%)
  2.  **Base:** $C_{raw}$
  3.  **Mid-Tone:** $C_{mid} = C \cdot 0.70$
  4.  **Deep Shadow:** $C_{shadow} = C \cdot 0.40$
* **Information Yield:**
  Essential for button states (Hover, Active, Pressed) and 3D texture assets. It reveals if a color "breaks" (shifts hue or desaturates too much) when mathematically darkened. For example, yellows often turn "muddy green" when simply multiplied by 0.7; this strip visualizes that failure case immediately.

#### B. Dithered Interpolation (Random Pairs)
* **Identifier:** `ID:25 (RANDOM PAIRS)`
* **Technical Operation:**
  Selects two random colors ($C_1, C_2$) and creates a vertical transition:
  * **Top:** $100\% C_1$
  * **Middle:** $50\% C_1 + 50\% C_2$ (via Checkerboard Dither)
  * **Bottom:** $100\% C_2$
* **Usage:**
  Tests **optical mixing**. Unlike the linear gradients in Module 2 (which calculated a new RGB value), this uses the eye's tendency to blend adjacent pixels. If the middle section flickers or creates an uncomfortable "shimmer" (chromostereopsis), those two colors are incompatible as foreground/background layers.

### 3. Usage & Inference
**Primary Use:** Game Development (Pixel Art/Retro), UI Interaction States, and Printing.

* **Button States:** Use `ID:23` to instantly grab the `Hover` (Row 1) and `Pressed` (Row 3) colors for any button in your UI without manually picking them.
* **Compression Safety:** `ID:21` helps predict how JPEG compression might artifact the edges of your colored elements.

---

## Module 5: Contour & Polar Analysis

### 1. Executive Summary
This module performs a **Topological Gradient Analysis** and a **Radial Saturation Check**. 

While previous modules analyzed colors as discrete flat blocks, Module 5 treats them as peaks in a continuous $Z$-field. It simulates how each color behaves when fading into the background (gradient banding checks) and maps the palette's angular density to identify specific hue-family biases (e.g., "Is this palette too heavy on Blue?").

### 2. Submodule Breakdown

#### A. Isoline Topology Grid (12-Bit Simulation)
* **Identifier:** `ID:24 (12-BIT COLSPACE)`
* **Technical Operation:**
  This 4x4 grid generates a scalar field $Z(x,y)$ for every palette color and renders it using discrete quantization steps (isolines). 
  
  * **Top 8 Cells (Radial):**
    Generated via a radial distance function with a sinusoidal perturbation:
    $$Z = \sqrt{(x-x_0)^2 + (y-y_0)^2} + 0.1 \cdot \sin(10x)$$
    This simulates a standard radial gradient with slight noise.
  * **Bottom 8 Cells (Interference):**
    Generated by summing orthogonal sine waves with random phase shifts (similar to Fourier synthesis):
    $$Z = \sum \sin(f_x \cdot x + \phi_x) \cdot \cos(f_y \cdot y + \phi_y)$$
  
* **Analysis:**
    * **Banding Detection:** The "stepped" rendering (contourf with 6-7 levels) mimics the "Banding" artifacts seen on low-bit-depth displays or compressed video streams. If the transition between bands looks jarring for a specific color, that color is prone to posterization artifacts.
    * **Contrast Linearity:** If the bands are tightly packed at the edge but loose in the center, the color has a non-linear falloff which may make shadows look unnatural.

#### B. Polar Saturation Plot
* **Identifier:** `ID:P01 (POLAR_SAT)`
* **Technical Operation:**
  A normalized polar projection of the HSV color space.
  
  * **Angular Coordinate ($\theta$):** Represents Hue ($0 \to 2\pi$).
  * **Radial Coordinate ($r$):** Represents **Relative Saturation**.
    $$r = \frac{S_{color}}{S_{max\_in\_palette}}$$
    *Note: This is normalized against the palette's own maximum saturation, not absolute saturation. The most saturated color in the set will always touch the outer rim.*
  
* **Rendering Technique (Density Integration):**
  Instead of drawing hard points, the module renders "soft alpha" particles.
  * **Overlap Glow:** When multiple colors occupy the same hue/saturation angle (e.g., three different Blues), their alpha channels sum up additively.
  * **Result:** Bright, glowing "hotspots" indicate high redundancy in that spectral region. Dark/thin areas indicate spectral gaps.

### 3. Usage & Inference
**Primary Use:** Gradient Design & Brand Identity Balancing.

* **Gap Analysis:** Look at `ID:P01`. If a large slice of the pie (e.g., the Yellow/Orange quadrant) is completely empty, the palette completely lacks warmth. This is acceptable for "Cold/Professional" themes but fatal for "Playful/Dynamic" themes.
* **Redundancy Check:** If you see a single blindingly white glowing spot in the Polar Plot, it means you have too many colors that are mathematically distinct but perceptually identical in terms of "Color Power" (Hue + Saturation). You should delete some of those duplicates.
* **Background Compatibility:** Inspect `ID:24`. If the outer contour ring (the darkest one) blends too invisibly into the background square, that color lacks sufficient "edge contrast" to be used as a glow or shadow effect on this specific background color.

---

## Module 6: Hybrid Gamut

### 1. Executive Summary
This module focuses on **3D lighting simulation** and **non-linear radial mapping**. It tests how the palette handles diffuse lighting on spherical surfaces and how it behaves under fisheye distortion.

### 2. Submodule Breakdown

#### A. Diffuse Lighting Simulation (Spheres)
* **Identifiers:** `ID:26`, `ID:27`
* **Technical Operation:**
  * **Constraint:** The Saturation is locked (at 60% or 80%).
  * **Mapping:** The theoretical pixel color is snapped to the nearest neighbor in the palette.
* **Analysis:**
  * **Shadow Banding:** Look at the "terminator line" (where light turns to shadow). If the transition is jagged or abrupt, the palette lacks sufficient dark variants of that hue.
  * **Specular Highlights:** Since this model is diffuse-only, any "shiny" spots appearing are artifacts of the palette having white/bright colors that are "too close" to the mid-tones.

#### B. Fisheye Lens Distortion (Bottom Row)
* **Identifiers:** `ID:28 (S:100%)`, `ID:29 (S:37%)`
* **Technical Operation:**
  This simulation applies a non-linear radial mapping to the color space, mimicking a wide-angle lens.
  
  * **Radial Mapping:**
    $$r_{fish} = \frac{\arcsin(r_{linear})}{\pi / 2}$$
  * **Gradient Logic:**
    * **Hue:** Defined by angle around the center.
    * **Brightness:** Decays linearly from center (1.0) to edge (0.1).
* **Information Yield:**
  * **Hue Dominance (ID:28):** At 100% saturation, this sphere shows the "purest" version of the palette. The color that occupies the largest slice of the pie is the dominant hue of the system.
  * **Gray Collapse (ID:29):** At 37% saturation, colors are very muted. If the sphere looks entirely gray with no discernible hue, the palette's low-saturation tokens are "washing out" (losing their chromatic identity).

### 3. Usage & Inference
**Primary Use:** 3D Texture Art, Icon Design, and Illustration.

* **Material Definition:** Use `ID:26` to judge if the palette can render "matte" materials (plastic, rubber, paper). If the sphere looks flat (like a 2D circle), the palette lacks the contrast range necessary for 3D illusion.
* **Gradient Smoothness:** Inspect the radial gradients in the Fisheye views.
    * **Good:** Concentric rings of color getting progressively darker.
    * **Bad:** "Speckling" or noise, where a dark pixel randomly appears inside a light ring. This indicates an inconsistency in the palette's luminance sorting (e.g., a "Dark Blue" that is mathematically brighter than a "Medium Blue").

---

## Module 7: Complementary Desaturation Planes

### 1. Executive Summary
This module analyzes **complementary color relationships** and **neutralization paths**. It tests how the palette handles transitions between opposing hues and how it defines its neutral (gray) spectrum.

### 2. Submodule Breakdown

#### A. The Six Axes of Conflict
The module tests the standard 12-point color wheel oppositions:
1.  **ID:30 (Red $\leftrightarrow$ Cyan):** The "Hot/Cold" axis.
2.  **ID:31 (Orange $\leftrightarrow$ Azure):** The "Warm/Cool" axis.
3.  **ID:32 (Yellow $\leftrightarrow$ Blue):** The "Day/Night" axis (critical for UI dark modes).
4.  **ID:33 (Chartreuse $\leftrightarrow$ Violet):** The "Acidic/Toxic" axis.
5.  **ID:34 (Green $\leftrightarrow$ Magenta):** The "Digital" axis (Sensor vs. Error).
6.  **ID:35 (Spring $\leftrightarrow$ Rose):** The "Flora" axis.

### 3. Usage & Inference
**Primary Use:** Data Visualization (Diverging Scales) and Semantic UI States.

#### A. The "Spine" Analysis (The Center Line)
Look closely at the vertical center line of each box where the saturation drops to zero.
* **The Zig-Zag Effect:** If the center line looks like a jagged zipper, your palette's neutral grays are not truly neutral. Some are "warm grays" (tinted orange) and some are "cool grays" (tinted blue). This inconsistency will make your UI look messy.
* **The Void:** If the center is just a solid vertical block of a single gray color, your palette lacks luminance definition in the neutral spectrum.

#### B. The "Bridge" Check
* **Smooth Transition:** If you see a gradient of "dusty" colors leading into the gray center, the palette is **Robust**. It contains low-saturation tokens (e.g., `Blue-Grey`, `Dusty-Pink`) that allow for subtle UI design.
* **Hard Snap:** If the colors stay vibrant until they instantly hit the gray wall (a sharp vertical line), the palette is **Brittle**. It lacks "tones" and "shades," forcing you to use high-saturation colors everywhere. This causes eye fatigue.

#### C. Data Viz Suitability
* **ID:30 (Red/Cyan)** and **ID:31 (Orange/Azure)** are the most critical for charts (e.g., Temperature maps, Financial gains/losses). If these panels look smooth, the palette is "Data-Ready."

---

## Module 8: Primary Ranges

### 1. Executive Summary
This module performs a **Hue-Specific Depth Audit**. While previous modules analyzed the palette as a whole or in relation to gradients, Module 8 dissects the color scheme into 9 discrete spectral slices.

It answers the question: **"How versatile is this palette within a specific color family?"** For example, if you are building a "Success" notification, you need Green. This module reveals if you have enough variation in Green to create a background, a border, and text, or if you only have one single "Green" token available.

### 2. Technical Breakdown

#### A. The Planar Slice Logic
* **Identifiers:** `ID:36` through `ID:44`
* **Mathematical Model:**
  Each of the 9 strips represents a 2D cross-section of the HSV color cylinder at a fixed Hue angle ($\theta$).
  
  * **X-Axis (Value/Brightness):** Ranges linearly from $0.0$ (Left/Black) to $1.0$ (Right/White).
  * **Y-Axis (Saturation):**
    Ranges linearly from $0.0$ (Bottom/Gray) to $1.0$ (Top/Vivid).

#### B. The Nearest-Neighbor Field
For every pixel $(x,y)$ in a strip fixed at Hue $\theta$:
1.  Calculate theoretical target: $C_{target} = HSV(\theta, y_{norm}, x_{norm})$
2.  Search the entire palette vector $P$ for the index $i$ that minimizes Euclidean distance:
    $$\min_i \| C_{target} - P_i \|^2$$
3.  Render pixel $(x,y)$ using color $P_i$.

### 3. Usage & Inference
**Primary Use:** UI State Definition & Illustration Guidelines.

#### A. The "Blue vs. The World" Check
* **Inspect `ID:41 (AZURE)` and `ID:42 (BLUE)`:** You will likely see complex, smooth shapes with many different shades. This indicates high fidelity in the blue spectrum.
* **Compare with `ID:36 (RED)`:** If the Red strip is mostly dominated by black/gray blocks with only a tiny patch of actual red at the top right, it confirms the palette treats Red purely as a functional "alert" color, not an aesthetic one.

#### B. The "Muddy Yellow" Warning
* **Inspect `ID:38 (YELLOW)`:** Yellow is mathematically difficult because dark yellow $(V < 0.5)$ is perceived as "Olive" or "Brown."
* **Diagnosis:** If the bottom-left of the Yellow strip looks greenish-brown, avoid using your yellow tokens on dark backgrounds, or they will look dirty.

#### C. Missing Channels (The Gray Wash)
* **Inspect `ID:44 (MAGENTA)` or `ID:37 (ORANGE)`:** In specialized palettes, these strips often look almost entirely grayscale.
* **Meaning:** If a strip is 90% gray, **do not** attempt to use that color for primary branding elements. The system simply lacks the mathematical definition to support gradients or shadows in that hue.

---
Developed by **albrp97**
