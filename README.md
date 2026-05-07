# 📸 Streamlit Photo Editor

A browser-based image editing tool built with **Streamlit**, **OpenCV**, and **PIL** that lets you apply a wide range of image transformations and visualize pixel data — all without writing a single line of code.

---

## Features

- **19 image transformations** including filters, color spaces, and artistic effects
- **Side-by-side comparison** of the original and processed image
- **Interactive controls** (sliders) for fine-tuning adjustable transformations
- **RGB histogram** rendered with Matplotlib
- **Pixel intensity distribution** chart powered by Plotly
- **One-click download** of the processed image as a PNG

---

## Transformations Available

| Category | Transformations |
|---|---|
| Basic | Grayscale, Flip Horizontal, Flip Vertical |
| Blur & Sharpen | Blur, Gaussian Blur, Sharpen |
| Edge Detection | Edge Detection, Canny Edge |
| Adjustments | Brightness, Contrast, Rotate, Resize, Threshold |
| Color | Sepia, HSV Color Space, Histogram Equalization |
| Artistic | Cartoon, Sketch |

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/streamlit-photo-editor.git
   cd streamlit-photo-editor
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`

---

## Requirements

```
streamlit
opencv-python
numpy
Pillow
matplotlib
plotly
pandas
```

Save these to a `requirements.txt` file in the project root.

---

## Usage

1. Launch the app and upload a `PNG`, `JPG`, or `JPEG` image.
2. Use the **sidebar** to select a transformation from the dropdown.
3. Adjust any sliders that appear (e.g., blur kernel size, brightness factor, rotation angle).
4. View the **original** and **processed** images side by side.
5. Explore the **RGB Histogram** and **Pixel Intensity Distribution** charts below.
6. Click **Download Image** to save the processed result.

---

## Project Structure

```
streamlit-photo-editor/
├── app.py           # Main application file
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## Screenshots

> _Upload your image, pick a transformation, and see results instantly._

| Original | Sketch | Cartoon |
|---|---|---|
| ![original](https://via.placeholder.com/200x150?text=Original) | ![sketch](https://via.placeholder.com/200x150?text=Sketch) | ![cartoon](https://via.placeholder.com/200x150?text=Cartoon) |

---

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI and app framework
- [OpenCV](https://opencv.org/) — Core image processing
- [Pillow](https://python-pillow.org/) — Brightness, contrast enhancements
- [Matplotlib](https://matplotlib.org/) — RGB histogram plotting
- [Plotly](https://plotly.com/python/) — Interactive pixel intensity chart
- [NumPy](https://numpy.org/) — Array operations

---

## License

This project is open source and available under the [MIT License](LICENSE).
