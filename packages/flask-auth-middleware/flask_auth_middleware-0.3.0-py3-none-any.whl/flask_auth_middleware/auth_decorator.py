from functools import wraps
from typing import Callable, List

import jwt
from flask import jsonify, make_response, request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def login_required(secret_key: str, algorithms: List[str] = ["HS256"]):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                authorization_header = request.headers.get("Authorization")
                if not authorization_header or not authorization_header.startswith(
                    "Bearer "
                ):
                    return make_response(
                        jsonify({"message": "Missing Authorization Header"}), 401
                    )

                access_token = request.headers["Authorization"].split(" ")[1]
                decoded_payload = jwt.decode(
                    access_token, key=secret_key, algorithms=algorithms
                )
                return func(decoded_payload, *args, **kwargs)
            except ExpiredSignatureError as exc:
                return make_response(
                    jsonify({"message": f"Token has expired. {str(exc)}"}), 401
                )
            except InvalidTokenError as exc:
                return make_response(
                    jsonify({"message": f"Invalid Token. {str(exc)}"}), 401
                )
            except Exception as exc:
                return make_response(jsonify({"message": str(exc)}), 500)

        return wrapper

    return decorator
