import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI App")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")


settings = Settings()
