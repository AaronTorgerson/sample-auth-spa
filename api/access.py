import json
from functools import wraps
from urllib.request import urlopen

from django.conf import settings
from django.core.exceptions import PermissionDenied
from jose import jwt


AUTH0_DOMAIN = settings.AUTH0_DOMAIN
API_AUDIENCE = settings.API_AUDIENCE
ALGORITHMS = ["RS256"]


def requires_scope(scope):
    """
    Determines if the Access Token is valid
    """
    def decorator(f):
        @wraps(f)
        def decorated(request, *args, **kwargs):
            token = get_token_auth_header(request)
            jsonurl = urlopen("https://" + settings.AUTH0_DOMAIN + "/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer="https://"+AUTH0_DOMAIN+"/"
                    )

                    if scope not in payload['scope']:
                        raise PermissionDenied({"code": "missing_required_scope",
                                                "description": "required scope was not present"}, 401)
                except jwt.ExpiredSignatureError:
                    raise PermissionDenied({"code": "token_expired",
                                            "description": "token is expired"}, 401)
                except jwt.JWTClaimsError:
                    raise PermissionDenied({"code": "invalid_claims",
                                            "description":
                                                "incorrect claims,"
                                                "please check the audience and issuer"}, 401)
                except Exception:
                    raise PermissionDenied({"code": "invalid_header",
                                            "description":
                                                "Unable to parse authentication"
                                                " token."}, 401)

                return f(request, access_token=payload, *args, **kwargs)
            raise PermissionDenied({"code": "invalid_header",
                                    "description": "Unable to find appropriate key"}, 401)

        return decorated
    return decorator


# Format error response and append status code
def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise PermissionDenied({"code": "authorization_header_missing",
                                "description":
                                    "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise PermissionDenied({"code": "invalid_header",
                                "description":
                                    "Authorization header must start with"
                                    " Bearer"}, 401)
    elif len(parts) == 1:
        raise PermissionDenied({"code": "invalid_header",
                                "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise PermissionDenied({"code": "invalid_header",
                                "description":
                                    "Authorization header must be"
                                    " Bearer token"}, 401)

    token = parts[1]
    return token

