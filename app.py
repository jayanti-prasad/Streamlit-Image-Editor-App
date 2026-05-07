# app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Streamlit Photo Editor",
    layout="wide"
)

# =========================
# Styling
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #111827;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #1f2937;
}

[data-testid="stFileUploader"] {
    background-color: #1f2937 !important;
    border: 2px dashed #4b5563 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

[data-testid="stFileUploader"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📸 Streamlit Photo Editor")

# =========================
# Upload Image
# =========================
uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.sidebar.header("🛠 Image Transformations")

    transform = st.sidebar.selectbox(
        "Select Transformation",
        [
            "Original",
            "Grayscale",
            "Blur",
            "Gaussian Blur",
            "Sharpen",
            "Edge Detection",
            "Canny Edge",
            "Brightness",
            "Contrast",
            "Rotate",
            "Flip Horizontal",
            "Flip Vertical",
            "Resize",
            "Threshold",
            "Sepia",
            "Cartoon",
            "Sketch",
            "HSV Color Space",
            "Histogram Equalization",
        ]
    )

    processed = img_np.copy()

    # =========================
    # Transformations
    # =========================

    if transform == "Grayscale":
        processed = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)

    elif transform == "Blur":
        k = st.sidebar.slider("Kernel Size", 1, 25, 5, step=2)
        processed = cv2.blur(processed, (k, k))

    elif transform == "Gaussian Blur":
        k = st.sidebar.slider("Kernel Size", 1, 25, 7, step=2)
        processed = cv2.GaussianBlur(processed, (k, k), 0)

    elif transform == "Sharpen":
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        processed = cv2.filter2D(processed, -1, kernel)

    elif transform == "Edge Detection":
        processed = cv2.Canny(processed, 100, 200)

    elif transform == "Canny Edge":
        t1 = st.sidebar.slider("Threshold 1", 0, 255, 100)
        t2 = st.sidebar.slider("Threshold 2", 0, 255, 200)
        processed = cv2.Canny(processed, t1, t2)

    elif transform == "Brightness":
        factor = st.sidebar.slider("Brightness", 0.1, 3.0, 1.2)
        pil_img = Image.fromarray(processed)
        enhancer = ImageEnhance.Brightness(pil_img)
        processed = np.array(enhancer.enhance(factor))

    elif transform == "Contrast":
        factor = st.sidebar.slider("Contrast", 0.1, 3.0, 1.5)
        pil_img = Image.fromarray(processed)
        enhancer = ImageEnhance.Contrast(pil_img)
        processed = np.array(enhancer.enhance(factor))

    elif transform == "Rotate":
        angle = st.sidebar.slider("Angle", -180, 180, 90)
        h, w = processed.shape[:2]
        matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
        processed = cv2.warpAffine(processed, matrix, (w, h))

    elif transform == "Flip Horizontal":
        processed = cv2.flip(processed, 1)

    elif transform == "Flip Vertical":
        processed = cv2.flip(processed, 0)

    elif transform == "Resize":
        width = st.sidebar.slider("Width", 50, 2000, image.width)
        height = st.sidebar.slider("Height", 50, 2000, image.height)
        processed = cv2.resize(processed, (width, height))

    elif transform == "Threshold":
        thresh = st.sidebar.slider("Threshold", 0, 255, 127)
        gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        _, processed = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)

    elif transform == "Sepia":
        kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])
        processed = cv2.transform(processed, kernel)
        processed = np.clip(processed, 0, 255).astype(np.uint8)

    elif transform == "Cartoon":
        gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)

        edges = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            9,
            9
        )

        color = cv2.bilateralFilter(processed, 9, 300, 300)
        processed = cv2.bitwise_and(color, color, mask=edges)

    elif transform == "Sketch":
        gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        inv_blur = 255 - blur
        processed = cv2.divide(gray, inv_blur, scale=256.0)

    elif transform == "HSV Color Space":
        processed = cv2.cvtColor(processed, cv2.COLOR_RGB2HSV)

    elif transform == "Histogram Equalization":
        gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        processed = cv2.equalizeHist(gray)

    # =========================
    # Layout
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Processed Image")

        if len(processed.shape) == 2:
            st.image(processed, clamp=True, use_container_width=True)
        else:
            st.image(processed, use_container_width=True)

    # =========================
    # Histogram
    # =========================

    st.subheader("📊 RGB Histogram")

    if len(processed.shape) == 3:

        fig, ax = plt.subplots(figsize=(8, 4))

        colors = ("r", "g", "b")

        for i, c in enumerate(colors):
            hist = cv2.calcHist([processed], [i], None, [256], [0, 256])
            ax.plot(hist, color=c)

        ax.set_xlim([0, 256])
        ax.set_title("Color Histogram")

        st.pyplot(fig)

    # =========================
    # Plotly Pixel Intensity
    # =========================

    st.subheader("📈 Pixel Intensity Distribution")

    flat_pixels = processed.flatten()

    df = pd.DataFrame({
        "Pixel Intensity": flat_pixels
    })

    fig_plotly = px.histogram(
        df,
        x="Pixel Intensity",
        nbins=50,
        title="Pixel Intensity Histogram"
    )

    st.plotly_chart(fig_plotly, use_container_width=True)

    # =========================
    # Download
    # =========================

    st.subheader("⬇ Download Processed Image")

    if len(processed.shape) == 2:
        output_img = Image.fromarray(processed)
    else:
        output_img = Image.fromarray(processed.astype(np.uint8))

    buf = BytesIO()
    output_img.save(buf, format="PNG")

    st.download_button(
        label="Download Image",
        data=buf.getvalue(),
        file_name="processed_image.png",
        mime="image/png"
    )

else:
    st.info("Upload an image to begin.")