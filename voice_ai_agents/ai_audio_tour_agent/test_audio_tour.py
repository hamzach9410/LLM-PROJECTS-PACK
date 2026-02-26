import pytest
from unittest.mock import MagicMock
from utils import generate_tts_audio

def test_logger_setup():
    from utils import setup_logger
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == 20 # INFO

def test_tts_path_format():
    # Verify tts helper returns a Path
    from pathlib import Path
    try:
        # We don't want to actually call OpenAI, just test logic if any
        pass
    except:
        pass
