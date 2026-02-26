import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# UI Constants
VOICE_OPTIONS = ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"]
INTEREST_OPTIONS = ["History", "Architecture", "Culinary", "Culture"]
VOICE_STYLE_OPTIONS = ["Friendly & Casual", "Professional & Detailed", "Enthusiastic & Energetic"]
DEFAULT_VOICE = "nova"
WORDS_PER_MINUTE = 150
