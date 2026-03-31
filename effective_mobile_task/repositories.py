from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User, RolePermission, RefreshToken

class BaseRepo:
    def __init__(self, db_session: Session):
        self.db_session = db_session

class UserRepo(BaseRepo):
    
    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db_session.get(User, user_id)
    
    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db_session.execute(stmt).scalar_one_or_none()
    
    def create_user(self, user: User) -> User:
        self.db_session.add(user)
        return user
    
    def update_user(self, user: User) -> User:
        return user
    
    def delete_user(self, user: User) -> None:
        self.db_session.delete(user)

class AuthRepo(BaseRepo):
        
    def get_refresh_token(self, token: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        return self.db_session.execute(stmt).scalar_one_or_none()
    
    def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db_session.add(refresh_token)
        return refresh_token
    
    def revoke_token(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked = True
    
    def get_active_tokens_for_user(self, user_id: int) -> list[RefreshToken]:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        )
        return self.db_session.execute(stmt).scalars().all()
    
    def revoke_all_user_tokens(self, user_id: int) -> None:
        tokens = self.get_active_tokens_for_user(user_id)
        for token in tokens:
            token.revoked = True



class PermissionRepo(BaseRepo):
    
    def get_permission_by_id(self, permission_id: int) -> RolePermission | None:
        return self.db_session.get(RolePermission, permission_id)
    
    def get_permission_by_name(self, name: str) -> RolePermission | None:
        stmt = select(RolePermission).where(RolePermission.name == name)
        return self.db_session.execute(stmt).scalar_one_or_none()
    
    def create_permission(self, permission: RolePermission) -> RolePermission:
        self.db_session.add(permission)
        return permission
    
    def update_permission(self, permission: RolePermission) -> RolePermission:
        return permission
    
    def delete_permission(self, permission: RolePermission) -> None:
        self.db_session.delete(permission)