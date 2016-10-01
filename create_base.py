from config import porg_config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(porg_config.DB_URL, echo=False)
Base = declarative_base(bind=engine)
