from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shopping_list.config import config

engine = create_engine(f'{config.DB_PROTOCOL}://{config.DB_SERVER}')
Session = sessionmaker(bind=engine)
