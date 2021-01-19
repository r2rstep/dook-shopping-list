from sqlalchemy.orm import Session

from ..domain import commands, fridge as fridge_models
from ..adapters.db import repo_sqlalchemy as repos, models as db_models
from .message_bus import g_message_bus


def update_fridge_contents(db: Session,
                           command: commands.ChangeFridgeContents,
                           fridge_id: int):
    fridge_db: db_models.Fridge
    fridge: fridge_models.Fridge
    fridge_db, fridge = repos.fridge.get(db, id=fridge_id)
    logic = fridge_models.FridgeLogic(fridge)
    logic.update_contents(command.products)
    repos.fridge.update(db, db_obj=fridge_db, obj_in=fridge)
    g_message_bus.notify(db, logic.events)
