import os

class Config:
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
