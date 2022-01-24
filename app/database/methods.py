from engine import session
from models import Store

async def get_nearest_stores(current_address):
    pass

async def add_store(address, image, name, description,coordinates=None):
    store = Store(name=name)
    session.add(store)
    session.commit()

async def add_like(store_id, user_from=None, positive=True):
    pass

async def get_likes(store_id):
    pass