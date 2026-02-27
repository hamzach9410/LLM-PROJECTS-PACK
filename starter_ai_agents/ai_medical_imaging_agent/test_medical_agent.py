import pytest
from PIL import Image as PILImage
from utils import resize_medical_image

def test_image_resizing():
    # Create a test image
    img = PILImage.new('RGB', (1000, 500))
    resized = resize_medical_image(img, target_width=500)
    assert resized.size == (500, 250)

def test_logger_setup():
    from utils import setup_logger
    logger = setup_logger("test_medical")
    assert logger.name == "test_medical"

def test_diagnostic_prompt():
    from agents_config import DIAGNOSTIC_PROMPT
    assert "Modality" in DIAGNOSTIC_PROMPT
    assert "Diagnostic Assessment" in DIAGNOSTIC_PROMPT
