from .adapters import db
from .domain.fridge import FridgeContentChanged
from .service.shopping_list import update_shopping_lists
from .service.message_bus import g_message_bus


events_handlers = {
    FridgeContentChanged: [update_shopping_lists]
}


def bootstrap():
    db.model_base.Base.metadata.create_all(bind=db.session.engine)


def register_handlers():
    for event_type, handlers in events_handlers.items():
        for handler in handlers:
            g_message_bus.subscribe(handler, event_type)
