import pytest
from utils import extract_meme_url

def test_extract_meme_url_standard():
    res = "The meme is at https://imgflip.com/i/abcd123"
    assert extract_meme_url(res) == "https://i.imgflip.com/abcd123.jpg"

def test_extract_meme_url_direct():
    res = "Direct link: https://i.imgflip.com/xyz987.png"
    assert extract_meme_url(res) == "https://i.imgflip.com/xyz987.png"

def test_extract_meme_url_none():
    assert extract_meme_url("no link here") is None

def test_config_logic():
    from agents_config import get_task_description
    task = get_task_description("test query")
    assert "test query" in task
    assert "https://imgflip.com/memetemplates" in task
