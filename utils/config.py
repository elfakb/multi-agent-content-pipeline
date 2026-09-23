import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    TEXT_MODEL = "gpt-4o"
    IMAGE_MODEL = "dall-e-3"
    VIDEO_MODEL = "sora-2"           # used only in the manual Video Studio step
    TEMPERATURE = 0.7

    OUTPUT_ROOT = "output"

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise EnvironmentError("Missing required environment variable: OPENAI_API_KEY")