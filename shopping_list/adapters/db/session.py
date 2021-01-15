from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:////tmp/test.db')    # TODO: make this configurable
Session = sessionmaker(bind=engine)
