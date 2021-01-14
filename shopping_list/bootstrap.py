from .adapters import db


def bootstrap():
    db.model_base.Base.metadata.create_all(bind=db.session.engine)
