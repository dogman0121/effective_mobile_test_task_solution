from functools import wraps
from flask import request
from flask_jwt_extended import (
    get_jwt_identity,
)
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import ExpiredSignatureError

from dependency_injector.wiring import inject, Provide

from .containers import AppContainer
from .services import UserService, JWTService
from .exceptions import ApiException, NotFoundException


def login_required(optional=False, refresh=False):
    def decorator(func):
        @wraps(func)
        @inject
        def wrapper(
            *args, 
            user_service: UserService = Provide[AppContainer.user_service],
            jwt_service: JWTService = Provide[AppContainer.jwt_service],
            **kwargs
        ):
            try:
                authorization_header = request.headers.get("Authorization")

                if authorization_header is None or not authorization_header.startswith("Bearer"):
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiException(status_code=401, error="unauthorized")
                
                token = authorization_header.replace("Bearer ", "").strip()

                user_id = jwt_service.decode_jwt(token)["user_id"]
                
                if user_id is None:
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiException(status_code=401, error="token_required", detail={"token": ["Missing authorization token"]})
                
                try:
                    user = user_service.get_user_by_id(user_id)

                    return func(user, *args, **kwargs)
                except NotFoundException:
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiException(status_code=401, error="invalid_token", detail={"token": ["Invalid authorization token"]})
            except ExpiredSignatureError as e:
                if optional:
                    return func(None, *args, **kwargs)
                raise e
            except JWTExtendedException:
                raise ApiException(status_code=401, error="invalid_token", detail={"token": ["Invalid authorization token"]})
        
        return wrapper
    return decorator