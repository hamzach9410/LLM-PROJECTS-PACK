import pytest
import os
from utils import get_file_extension

def test_get_file_extension():
    assert get_file_extension("test.MP4") == "mp4"
    assert get_file_extension("/path/to/image.jpg") == "jpg"
    assert get_file_extension("no_ext") == ""

def test_media_processor_type_mapping():
    from media_processor import MediaProcessor
    from agno.media import Image, Video, Document
    
    assert isinstance(MediaProcessor.get_agno_media("t.jpg", "jpg"), Image)
    assert isinstance(MediaProcessor.get_agno_media("t.mp4", "mp4"), Video)
    assert isinstance(MediaProcessor.get_agno_media("t.pdf", "pdf"), Document)

def test_logger_setup():
    from utils import setup_logger
    logger = setup_logger("test_multimodal")
    assert logger.name == "test_multimodal"
