import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///digests.db"
