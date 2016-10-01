from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///porg.db', echo=False)
Base = declarative_base(bind=engine)

# Initialise SQLAlchemy session
Base.metadata.create_all()
Session = sessionmaker(bind=engine)
s = Session()
