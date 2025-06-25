import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import cv2
import io

# Page Config
st.set_page_config(page_title="Custom Image Filters", layout="wide")
st.title("Kalm Photo Editor")
st.write("Upload an image and apply multiple filters with custom settings.")

# --- Functions ---
def apply_filters(image, selected_filters, intensity_values):
    """Apply multiple filters sequentially."""
    filtered_img = image.copy()
    
    for filter_name in selected_filters:
        intensity = intensity_values.get(filter_name, 1.0)
        
        if filter_name == "Blur":
            filtered_img = filtered_img.filter(ImageFilter.GaussianBlur(intensity))
        
        elif filter_name == "Sharpen":
            filtered_img = filtered_img.filter(ImageFilter.SHARPEN)
        
        elif filter_name == "Edge Enhance":
            filtered_img = filtered_img.filter(ImageFilter.EDGE_ENHANCE)
        
        elif filter_name == "Black & White":
            filtered_img = filtered_img.convert('L')
        
        elif filter_name == "Sepia":
            sepia_filter = ImageEnhance.Color(filtered_img)
            filtered_img = sepia_filter.enhance(0.5)
        
        elif filter_name == "Brightness":
            enhancer = ImageEnhance.Brightness(filtered_img)
            filtered_img = enhancer.enhance(intensity)
        
        elif filter_name == "Contrast":
            enhancer = ImageEnhance.Contrast(filtered_img)
            filtered_img = enhancer.enhance(intensity)
        
        elif filter_name == "Saturation":
            enhancer = ImageEnhance.Color(filtered_img)
            filtered_img = enhancer.enhance(intensity)
        
        elif filter_name == "Sketch":
            img_array = np.array(filtered_img)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            inverted = 255 - gray
            blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
            inverted_blurred = 255 - blurred
            sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
            filtered_img = Image.fromarray(sketch)
        
        elif filter_name == "Oil Painting":
            img_array = np.array(filtered_img)
            res = cv2.xphoto.oilPainting(img_array, 7, 1)
            filtered_img = Image.fromarray(res)
        
        elif filter_name == "Invert Colors":
            filtered_img = ImageOps.invert(filtered_img)
    
    return filtered_img

# --- Sidebar (Filter Selection) ---
st.sidebar.header("🛠 Custom Filters")

# Available filters
available_filters = [
    "Blur",
    "Sharpen",
    "Edge Enhance",
    "Black & White",
    "Sepia",
    "Brightness",
    "Contrast",
    "Saturation",
    "Sketch",
    "Oil Painting",
    "Invert Colors"
]

# Let users select multiple filters
selected_filters = st.sidebar.multiselect(
    "Choose filters to apply:",
    available_filters,
    default=["Blur", "Brightness"]
)

# Intensity sliders for selected filters
intensity_values = {}
for filter_name in selected_filters:
    if filter_name in ["Blur", "Brightness", "Contrast", "Saturation"]:
        intensity = st.sidebar.slider(
            f"{filter_name} Intensity",
            min_value=0.1,
            max_value=3.0,
            value=1.0,
            step=0.1,
            key=f"intensity_{filter_name}"
        )
        intensity_values[filter_name] = intensity

# --- Main App ---
uploaded_file = st.file_uploader("Upload an image (JPG, PNG, JPEG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    original_img = Image.open(uploaded_file)
    
    # Display original and filtered images side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(original_img, use_column_width=True)
    
    with col2:
        st.subheader("Filtered Image")
        if selected_filters:
            filtered_img = apply_filters(original_img, selected_filters, intensity_values)
            st.image(filtered_img, use_column_width=True)
            
            # Download button
            buf = io.BytesIO()
            filtered_img.save(buf, format="PNG")
            byte_img = buf.getvalue()
            
            st.download_button(
                "⬇️ Download Filtered Image",
                byte_img,
                file_name=f"filtered_{uploaded_file.name}",
                mime="image/png"
            )
        else:
            st.warning("No filters selected. Choose filters in the sidebar.")
else:
    st.info("Please upload an image to get started.")
