import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://atlas_user:your_password@localhost:5432/human_aging_atlas"
    )
    APP_NAME: str = "Human Aging Atlas API"
    APP_VERSION: str = "1.0.0"

settings = Settings()