from typing import Dict, Callable, Type, List

import attr
from sqlalchemy.orm import Session

from ..domain.event import Event


@attr.s(auto_attribs=True)
class MessageBus:
    _handlers: Dict[Type[Event], List[Callable]] = attr.ib(factory=dict)

    def subscribe(self, handler: Callable, event_type: Type[Event]):
        if event_type in self._handlers:
            self._handlers[event_type].append(handler)
        else:
            self._handlers[event_type] = [handler]

    def notify(self, db: Session, events: List[Event]):
        for event in events:
            for handler in self._handlers[type(event)]:
                handler(db, event)


g_message_bus = MessageBus()
