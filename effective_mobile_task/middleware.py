from functools import wraps
from flask import request
from flask_jwt_extended import (
    get_jwt_identity,
)
from flask_jwt_extended import (verify_jwt_in_request, get_jwt_identity)
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import ExpiredSignatureError

from dependency_injector.wiring import inject, Provide

from .containers import AppContainer
from .services import UserService
from .exceptions import ApiException, NotFoundException

def login_required(optional=False, refresh=False):
    def decorator(func):
        @wraps(func)
        @inject
        def wrapper(
            *args, 
            user_service: UserService = Provide[AppContainer.user_service],
            **kwargs
        ):
            try:
                verify_jwt_in_request(optional=optional, refresh=refresh, locations=["headers"])

                user_id = get_jwt_identity()
                
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