from werkzeug.security import generate_password_hash, check_password_hash
import jwt


from .repositories import UserRepo, AuthRepo, PermissionRepo
from .dto import UserUpdateDTO, UserCreateDTO, RegisterDTO, LoginDTO
from .models import User, ADMIN_ROLE, RolePermission
from .utils import DBTransaction
from .exceptions import NotFoundException, PermissionDeniedException, NotAuthorizedException

class HashService:
    
    def __init__(self):
        pass

    def generate_password_hash(self, password):
        return generate_password_hash(password)

    def check_password_hash(self, password, password_hash):
        return check_password_hash(password_hash, password)

class JWTService:

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encode_jwt(self, data: dict):
        return jwt.encode(data, key=self.secret_key.encode(), algorithm="HS256")

    def decode_jwt(self, token):
        return jwt.decode(token, key=self.secret_key.encode(), algorithms=["HS256"])

class UserService:
    
    def __init__(
        self, 
        user_repo: UserRepo,
        db_transaction: DBTransaction
    ):
        self.user_repo = user_repo
        self.db_transaction = db_transaction

    def get_user_by_id(self, user_id):
        user = self.user_repo.get_user_by_id(user_id)

        if user is None:
            raise NotFoundException
        
        return user
    
    def get_user_by_email(self, email):
        user = self.user_repo.get_user_by_email(email)

        if user is None:
            raise NotFoundException
        
        return user

    def create_user(self, data: UserCreateDTO):
        user = User(
            name=data.name,
            last_name=data.last_name,
            email=data.email,
            password=data.password_hash
        )

        with self.db_transaction:
            self.user_repo.create_user(user)

        return user

    def update_user(self, current_user, user, data: UserUpdateDTO):
        if current_user.id != user.id:
            raise PermissionDeniedException
        
        user.name = data.name
        user.last_name = data.last_name
        user.email = data.email
        
        with self.db_transaction:
            self.user_repo.update_user(user)

        return user
    
    def delete_user(self, current_user, user):
        if current_user.id != user.id:
            raise PermissionDeniedException
        
        user.is_active = True

        with self.db_transaction:
            self.user_repo.update_user()


class AuthService:
    def __init__(
        self, 
        auth_repo: AuthRepo, 
        user_repo: UserService,
        jwt_service: JWTService,
        hash_service: HashService,
        db_transaction: DBTransaction
    ):
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.jwt_service = jwt_service
        self.hash_service = hash_service
        self.db_transaction = db_transaction

    def register(self, data: RegisterDTO):
        password_hash = self.hash_service.generate_password_hash(data.password)

        user = User(
            name=data.name,
            last_name=data.last_name,
            email=data.email,
            password=password_hash
        )

        with self.db_transaction:
            self.user_repo.create_user(user)

        return self.jwt_service.encode_jwt({"user_id": user.id})

    def login(self, data: LoginDTO):
        user = self.user_repo.get_user_by_email(data.email)
        print(user.password, data.password)

        if self.hash_service.check_password_hash(data.password, user.password):
            return self.jwt_service.encode_jwt({"user_id": user.id})
        
        raise NotAuthorizedException

    def logout(self, user):
        pass
    
class PermissionService:
    def __init__(self, permission_repo: PermissionRepo, db_transaction: DBTransaction):
        self.permission_repo = permission_repo
        self.db_transaction=db_transaction

    def create_permission(self, user, data):
        if not user.role >= ADMIN_ROLE:
            raise PermissionDeniedException

        permission = RolePermission(
            name=data.name,
            role=data.role
        )

        with self.db_transaction:
            self.permission_repo.create_permission(permission)

        return permission

    def update_permission(self, user, permission, data):
        if not user.role >= ADMIN_ROLE:
            raise PermissionDeniedException
        
        permission.name = data.name
        permission.role = data.role
    
        with self.db_transaction:
            self.permission_repo.update_permission(permission)

        return permission

    def delete_permission(self, user, permission):
        if not user.role >= ADMIN_ROLE:
            raise PermissionDeniedException
        
        self.permission_repo.delete_permission(permission)