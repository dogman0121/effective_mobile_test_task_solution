
from dependency_injector import containers, providers

from .utils import DBTransaction
from .repositories import UserRepo, AuthRepo, PermissionRepo
from .services import HashService, JWTService, UserService, AuthService, PermissionService


class AppContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        [
            "effective_mobile_task.routes",
            "effective_mobile_task.middleware",
        ]
    )

    config = providers.Configuration()
    
    db_session = providers.Dependency()

    db_transaction = providers.Singleton(
        DBTransaction,
        db_session=db_session
    )

    user_repo = providers.Singleton(
        UserRepo,
        db_session=db_session
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
        db_transaction=db_transaction
    )

    auth_repo = providers.Singleton(
        AuthRepo,
        db_session=db_session
    )

    hash_service = providers.Singleton(
        HashService
    )

    jwt_service = providers.Singleton(
        JWTService,
        secret_key=config.SECRET_KEY
    )

    auth_service = providers.Factory(
        AuthService,
        auth_repo=auth_repo,
        hash_service=hash_service,
        jwt_service=jwt_service,
        user_repo=user_repo,
        db_transaction=db_transaction
    )

    permission_repo = providers.Singleton(
        PermissionRepo,
        db_session=db_session
    )

    permission_service = providers.Factory(
        PermissionService,
        permission_repo=permission_repo,
        db_transaction=db_transaction
    )