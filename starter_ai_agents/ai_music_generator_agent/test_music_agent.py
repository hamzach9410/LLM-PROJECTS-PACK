import pytest
import os
from utils import setup_logger, ensure_dir

def test_ensure_dir():
    test_dir = "test_audio_dir"
    if os.path.exists(test_dir):
        os.removedirs(test_dir)
    ensure_dir(test_dir)
    assert os.path.exists(test_dir)
    os.rmdir(test_dir)

def test_logger_setup():
    logger = setup_logger("test_music")
    assert logger.name == "test_music"
    assert logger.level == 20 # INFO

def test_agents_init():
    from agents_config import get_music_composer_agent
    agent = get_music_composer_agent("fake_key", "fake_key")
    assert agent.name == "Audio Maestro"
    assert agent.agent_id == "ml_music_composer"
