from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shopping_list.config import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
