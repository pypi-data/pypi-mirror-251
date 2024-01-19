from typing import Literal
import json
from pydantic import BaseModel
import ramda as R
from . import get

class RSAJWK(BaseModel):
    kid: str
    kty: Literal['RSA']
    e: str
    n: str

async def jwk(jwks_uri: str, kid: str) -> RSAJWK:
    content = await get(jwks_uri)
    jwks = json.loads(content)
    jwk = R.find(lambda jwk: jwk.get('kid') == kid, jwks['keys'])
    return RSAJWK.model_validate(jwk)
