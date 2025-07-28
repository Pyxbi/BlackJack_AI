from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

FIREWORKS_API_KEY = os.getenv('FIREWORKS_API_KEY')



# Game Configuration
DEFAULT_BALANCE = 1000
DEFAULT_BET = 100
GAME_PORT = 5100

# AI Configuration
AI_THINKING_TIME = 1.5  # seconds to simulate AI thinking
AI_AGGRESSIVENESS = 0.7  # 0.0 = conservative, 1.0 = aggressive

# Debug Configuration
DEBUG_MODE = True
LOG_AI_DECISIONS = True 