import os
import logging
from pathlib import Path
from openai import OpenAI
from typing import Optional

def setup_logger(name: str) -> logging.Logger:
    """Setup a standard logger with consistent formatting."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def generate_tts_audio(text: str, voice: str = "nova", speed: float = 1.0) -> Path:
    """
    Generate audio from text using OpenAI TTS.
    
    Args:
        text (str): The text to narrate.
        voice (str): OpenAI voice ID.
        speed (float): Playback speed (0.25 to 4.0).
        
    Returns:
        Path: Path to the generated audio file.
    """
    client = OpenAI()
    speech_file_path = Path(os.getcwd()) / "speech_tour.mp3"
    
    # Custom instructions for the TTS model
    instructions = (
        "You are a friendly and engaging tour guide. Speak naturally and conversationally, "
        "as if you're walking alongside the visitor. Use a warm, inviting tone. "
        "Maintain an enthusiastic but relaxed pace."
    )
        
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        speed=speed,
        instructions=instructions
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path
