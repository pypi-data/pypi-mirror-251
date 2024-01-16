import jwt
from . import util

async def authorize(
    token: str, app_id: str, tenant: str, policy: str
) -> dict[str, str]:
    meta = await util.metadata(tenant, policy)
    kid = jwt.get_unverified_header(token)['kid']
    jwk = await util.jwk(meta.jwks_uri, kid)
    pkey = util.rsa_pem(jwk.n, jwk.e)
    return jwt.decode(
        jwt=token,
        key=pkey,
        verify=True,
        algorithms=['RS256'],
        audience=app_id,
        issuer=meta.issuer,
    )
