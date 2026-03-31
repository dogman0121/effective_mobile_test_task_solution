from flask import Blueprint, request, jsonify
from dependency_injector.wiring import Provide, inject

from .schemas import (
    RegisterSchema, 
    LoginSchema, 
    UserSchema, 
    UserUpdateSchema, 
    PermissionSchema,
    PermissionCreateSchema,
    PermissionUpdateSchema
)
from .dto import (
    RegisterDTO, 
    LoginDTO, 
    UserUpdateDTO,
    PermissionCreateDTO,
    PermissionUpdateDTO
)
from .services import AuthService, UserService, PermissionService
from .containers import AppContainer
from .middleware import login_required
from .exceptions import ApiException, NotFoundException, PermissionDeniedException, NotAuthorizedException

bp = Blueprint('main', __name__)

@bp.errorhandler(Exception)
def error_handler(exception):
    print(exception)
    if isinstance(exception, ApiException):
        return jsonify({
            "error": exception.error,
            "detail": exception.detail
        }), exception.status_code
        
    return jsonify({
        "error": "internal_error",
        "detail": {}
    }), 500
    

@bp.route("/register", methods=["POST"])
@inject
def register_route(
    auth_service: AuthService = Provide[AppContainer.auth_service]
):
    register_schema = RegisterSchema().load(request.json)

    register_dto = RegisterDTO(
        name=register_schema.get("name"),
        last_name=register_schema.get("last_name"),
        email=register_schema.get("email"),
        password=register_schema.get("password")
    )

    token = auth_service.register(register_dto)

    return jsonify(
        {
            "token": token,
        }
    )



@bp.route("/login", methods=["POST"])
@inject
def login_route(
    auth_service: AuthService = Provide[AppContainer.auth_service]
):
    login_schema = LoginSchema().load(request.json)

    login_dto = LoginDTO(
        email=login_schema.get("email"),
        password=login_schema.get("password")
    )

    try:
        token = auth_service.login(login_dto)
    except NotAuthorizedException:
        raise ApiException(status_code=401, error="unauthorized")
    except NotFoundException:
        raise ApiException(status_code=404, error="not_found")

    return jsonify(
        {
            "token": token,
        }
    )

@bp.route("/logout", methods=["POST"])
@login_required()
@inject
def logout(
    current_user,
    auth_service: AuthService = Provide[AppContainer.auth_service]
):
    
    auth_service.logout(current_user)

@bp.route("/refresh", methods=["POST"])
@login_required(refresh=True)
def refresh_token_route(
    current_user,
    auth_service: AuthService = Provide[AppContainer.auth_service]
):
    tokens = auth_service.refresh_user_token(current_user)

    return jsonify(
        {
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token")
        }
    )

@bp.route("/users/<int:user_id>", methods=["GET"])
@inject
def get_user_route(
    user_id,
    user_service: UserService = Provide[AppContainer.user_service]
):
    try:
        user = user_service.get_user_by_id(user_id)
    except:
        raise ApiException(404, error="user_not_found")
    
    return jsonify({
        "data": UserSchema().dump(user)
    })
    

@bp.route("/users/<int:user_id>", methods=["PUT"])
@login_required()
@inject
def update_user_route(
    current_user,
    user_id,
    user_service: UserService = Provide[AppContainer.user_service]
):
    try:
        user = user_service.get_user_by_id(user_id)

        update_schema = UserUpdateSchema().load(request.json)

        update_dto = UserUpdateDTO(
            name=update_schema.get("name"),
            last_name=update_schema.get("last_name"),
            email=update_schema.get("email"),
        )

        updated_user = user_service.update_user(current_user, user, update_dto)

        return jsonify({
            "data": UserSchema().dump(updated_user)
        })

    except NotFoundException:
        raise ApiException(status_code=404, error="not_found")
    except PermissionDeniedException:
        raise ApiException(status_code=403, error="forbidden")

@bp.route("/users/<int:user_id>", methods=["DELETE"])
@login_required()
@inject
def delete_user_route(
    current_user,
    user_id,
    user_service: UserService = Provide[AppContainer.user_service]
):
    try:
        user = user_service.get_user_by_id(user_id)

        user_service.delete_user(current_user, user)

        return jsonify({
            "data": {
                "success": True
            }
        })

    except NotFoundException:
        raise ApiException(status_code=404, error="not_found")
    except PermissionDeniedException:
        raise ApiException(status_code=403, error="forbidden")

@bp.route("/permissions/<int:permission_id>", methods=["GET"])
@login_required()
@inject
def get_permission_route(
    current_user,
    permission_id,
    permission_service: PermissionService = Provide[AppContainer.permission_service]
):
    try: 
        permission = permission_service.get_permission_by_id(current_user, permission_id)

        return jsonify({
            "data": PermissionSchema.dump(permission)
        })
    except NotFoundException:
        raise ApiException(status_code=404, error="not_found")
    except PermissionDeniedException:
        raise ApiException(status_code=403, error="forbidden")

@bp.route("/permissions", methods=["POST"])
@login_required()
@inject
def create_permission_route(
    current_user,
    permission_service: PermissionService = Provide[AppContainer.permission_service]
):
    try: 
        create_schema = PermissionCreateSchema().load(request.json)

        create_dto = PermissionCreateDTO(
            name=create_schema.get("name"),
            role=create_schema.get("role")
        )

        permission = permission_service.create_permission(current_user, create_dto)

        return jsonify({
            "data": PermissionSchema.dump(permission)
        })
    except NotFoundException:
        raise ApiException(status_code=404, error="not_found")
    except PermissionDeniedException:
        raise ApiException(status_code=403, error="forbidden")

@bp.route("/permissions/<int:permission_id>", methods=["PUT"])
@login_required()
@inject
def update_permission_route(
    current_user,
    permission_id,
    permission_service: PermissionService = Provide[AppContainer.permission_service]
):
    try: 
        permission = permission_service.get_permission_by_id(current_user, permission_id)

        update_schema = PermissionUpdateSchema().load(request.json)

        update_dto = PermissionUpdateDTO(
            name=update_schema.get("name"),
            role=update_schema.get("role")
        )

        updated_permission = permission_service.update_permission(current_user, permission, update_dto)

        return jsonify({
            "data": PermissionSchema.dump(updated_permission)
        })
    except NotFoundException:
        raise ApiException(status_code=404, error="not_found")
    except PermissionDeniedException:
        raise ApiException(status_code=403, error="forbidden")

@bp.route("/permissions/<int:permission_id>", methods=["DELETE"])
@inject
def delete_permission_route(
    current_user,
    permission_id,
    permission_service: PermissionService = Provide[AppContainer.permission_service]
):
    try: 
        permission = permission_service.get_permission_by_id(current_user, permission_id)

        permission_service.delete_permission(current_user, permission)

        return jsonify({
            "data": {
                "success": True
            }
        })
    except NotFoundException:
        raise ApiException(status_code=404, error="not_found")
    except PermissionDeniedException:
        raise ApiException(status_code=403, error="forbidden")
