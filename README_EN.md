[🇷🇺 Русский](README.md) • [🇬🇧 English](README_EN.md)

<div align="center">

# 🔢 Animated Captcha Generator

**Python • Pillow • NumPy • SciPy**

A flexible and powerful captcha generator for creating static (PNG) and animated (GIF) images. It builds complex, OCR-resistant captchas using mathematical distortions, Bezier curves, and dynamic blurring.

<br>

[![Stars](https://img.shields.io/github/stars/A-R-E-S/animated-captcha-generator?style=social)](https://github.com/A-R-E-S/animated-captcha-generator/stargazers)
[![Forks](https://img.shields.io/github/forks/A-R-E-S/animated-captcha-generator?style=social)](https://github.com/A-R-E-S/animated-captcha-generator/network/members)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-11.0+-7c4dff?style=flat-square&logo=pillow&logoColor=white)](https://python-pillow.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.0+-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.14+-0054a6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 🎬 What it looks like

<p align="center">
  <img src="captchas/demo.gif" width="320" alt="Animated GIF captcha example"/>
  <br>
  <em>Animated captcha example (digits bounce, blur strip slides)</em>
</p>

---

## ✨ Features

- 📦 **Two formats:** Generates static images (`.png`) and animations (`.gif`).
- 🎨 **13 built-in fonts:** Papyrus, Book Antiqua, Mistral, Captcha Code, Courier New (including bold/italic), LED Dot Matrix, Lucida Handwriting, Tahoma, etc.
- 🌀 **Mathematical distortions:**
  - Random Bezier curves in the background (based on Bernstein polynomials).
  - Sine wave text trajectory.
  - Random rotation for each character (up to 60 degrees).
- 🎞️ **Animation (GIF):**
  - "Bouncing" digits effect with random phase and amplitude.
  - Seamless sliding Gaussian blur strip.
- 🛠️ **Fully customizable:** All parameters (size, color, curve points, blur amplitude, etc.) are at the top of the script.

---

## 📸 Screenshots

| 🖼️ Static Captcha (PNG) | 🎞️ Animation Frame (GIF) |
|:---:|:---:|
| <img src="captchas/example.png" width="280"/> | <img src="captchas/example_frame.png" width="280"/> |

---

## 🚀 Installation & Usage

### Requirements
- Python 3.10+
- Libraries: `Pillow`, `NumPy`, `SciPy`

### Steps

1. Clone the repository:
```bash
git clone https://github.com/A-R-E-S/animated-captcha-generator.git
cd animated-captcha-generator
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
# source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install pillow numpy scipy
```

4. Run the script:
```bash
python captcha_generator.py
```

5. Follow the console prompts:
```text
Captcha format (png / gif): gif
How many captchas to generate: 5
```
The generated files will be saved in the `captchas/` folder.

---

## ⚙️ Configuration

All main parameters are located in the `PARAMETERS FOR CONFIGURATION` block at the top of the `captcha_generator.py` file. You can easily change:

- `IMAGE_WIDTH`, `IMAGE_HEIGHT`: Output image dimensions.
- `MAX_ROTATION_ANGLE`: Maximum digit tilt angle.
- `FONT_SIZE`: Font size.
- `GIF_FRAMES`, `GIF_FRAME_DURATION`: Number of frames and GIF playback speed.
- `BLUR_RECT_DIRECTION`: Blur strip movement direction (`1` = right, `-1` = left).

> ⚠️ **Note:** For the script to work, font files (`.ttf`, `.otf`) must be in the same folder as the script itself.

## 📄 License

The project is distributed under the [MIT](LICENSE) license.

---

<div align="center">

### If you found this project helpful — give it a ⭐

</div>