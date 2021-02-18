import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = "1999x.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "Code4UDACITY"

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    myToken = request.headers.get("Authorization", None);
    if (not(myToken)): raise AuthError({
        "message": "Missing Header"
        }, 401);
    else:
        if (len(myToken.split()) != 2): raise AuthError({
            "message": "Invalid Header"
            }, 401);
        elif (myToken.split()[0].lower() != "bearer"): raise AuthError({
            "message": "Invalid Header"
            }, 401);
        else: return myToken.split()[1];

def check_permissions(permission, payload):
    if (not("permissions" in payload)): raise AuthError({
        "message": "Invalid Token"
        }, 401);
    elif (not(permission in payload["permissions"])): raise AuthError({
        "message": "Unauthorized"
        }, 401);
    else: return True;

def verify_decode_jwt(_T):
    JSON_JWKS = json.loads(urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json").read());
    if (not("kid" in jwt.get_unverified_header(_T))): raise AuthError({
        "message": "Invalid Header"
        }, 401);
    else:
        for oneKey in JSON_JWKS["keys"]:
            if (oneKey["kid"] == jwt.get_unverified_header(_T)["kid"]):
                RSA_KEYS = { "kty": oneKey["kty"], "kid": oneKey["kid"], "use": oneKey["use"], "n": oneKey["n"], "e": oneKey["e"] };
        try:
            PAYLOAD = jwt.decode(_T, RSA_KEYS, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer="https://" + AUTH0_DOMAIN + "/");
            return PAYLOAD;
        except: raise AuthError({
            "message": "Unauthorized Token"
            }, 401);

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
