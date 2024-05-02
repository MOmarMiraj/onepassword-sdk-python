from .core import _invoke
from json import loads
from .types import Item


class Items:
    def __init__(self, client_id):
        self.client_id = client_id

    async def create(self, item):
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Create",
                    "parameters": {
                        "item": item.dict(),
                    },
                },
            }
        )
        result = Item(**loads(response))
        return result

    async def get(self, vault_id, item_id):
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Get",
                    "parameters": {
                        "item_id": item_id,
                        "vault_id": vault_id,
                    },
                },
            }
        )
        result = Item(**loads(response))
        return result

    async def update(self, item):
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Update",
                    "parameters": {
                        "item": item.dict(),
                    },
                },
            }
        )
        result = Item(**loads(response))
        return result

    async def delete(self, vault_id, item_id):
        await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Delete",
                    "parameters": {
                        "vault_id": vault_id,
                        "item_id": item_id,
                    },
                },
            }
        )
