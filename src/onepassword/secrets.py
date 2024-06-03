from .core import _invoke
from json import loads


class Secrets:
    """
    Read more about secrets: https://developer.1password.com/docs/cli/secret-references

    Secrets point to fields in 1Password. They have the following format: op://<vault-name>/<item-name>[/<section-name>]/<field-name>
    """

    def __init__(self, client_id):
        self.client_id = client_id

    async def resolve(self, secret_reference):
        """Resolve returns the secret the provided secret reference points to."""
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Resolve",
                    "parameters": {
                        "secret_reference": secret_reference,
                    },
                },
            }
        )
        return str(loads(response))
