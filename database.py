from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
os.environ['POSTGRES_PASSWORD'] = '2012'


DATABASE_URL = f"postgresql://postgres:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/fastapi_auth"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

