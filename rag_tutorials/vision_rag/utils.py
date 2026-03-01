import PIL.Image
import io
import base64
import streamlit as st

MAX_PIXELS = 1568 * 1568

def resize_image_if_needed(pil_img):
    """Ensure image stays within multimodal embedding limits."""
    w, h = pil_img.size
    if w * h > MAX_PIXELS:
        scale = (MAX_PIXELS / (w * h)) ** 0.5
        pil_img.thumbnail((int(w * scale), int(h * scale)))

def pil_to_base64_data(pil_img):
    """Convert PIL image to base64 for Cohere API."""
    fmt = pil_img.format if pil_img.format else "PNG"
    resize_image_if_needed(pil_img)
    with io.BytesIO() as buf:
        pil_img.save(buf, format=fmt)
        return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def init_vision_session():
    """Initialize multimodal session state."""
    defaults = {
        'image_paths': [],
        'doc_embeddings': None,
        'cohere_key': "",
        'google_key': ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_vision_style():
    """Apply high-end creative studio aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #fafafa; }
        .stImage { border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_content_type=True)
