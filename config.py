import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Database configuration
DATABASE_URL = "sqlite:///devcore.db"

# Bot persona and other settings
DEVCORE_NAME = "DevCore"
DEVCORE_ROLE = "Elite engineering mentor"
DEVCORE_PERSONALITY = "Senior engineer + strategic mentor hybrid"
DEVCORE_TONE = "Direct, dense, authoritative"

# Adaptive learning settings
WEAK_AREA_THRESHOLD = 0.70  # 70%
CONSISTENT_HIGH_SCORE_THRESHOLD = 0.90 # 90%
SKILL_ASSESSMENT_QUIZ_QUESTIONS = 10
PROGRESS_REPORT_INTERVAL = 5 # Every 5 sessions

# AI API settings
# Set AI_PROVIDER to 'openai' or 'xai'
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
OPENAI_MODEL = "gpt-4"
XAI_MODEL = "grok-beta" # or current grok model
MAX_CONTEXT_TOKENS = 3000

# Code execution sandbox settings
CODE_EXECUTION_TIMEOUT = 10 # seconds

# Anti-passivity settings
SILENT_TIMEOUT_HOURS = 48
DIRECT_ANSWER_LOCK_COUNT = 3
DIRECT_ANSWER_LOCK_DURATION_MINS = 10

# Interview simulation settings
INTERVIEW_DURATION_MINS = 45

# Logging
LOG_FILE = "errors.log"
