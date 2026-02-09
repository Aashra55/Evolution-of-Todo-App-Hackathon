from sqlmodel import create_engine, Session, SQLModel
from os import environ
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from sqlmodel import create_engine, Session, SQLModel
from os import environ
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
DATABASE_URL = environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)