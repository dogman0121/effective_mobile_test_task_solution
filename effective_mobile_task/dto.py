from dataclasses import dataclass


@dataclass
class RegisterDTO:
    name: str
    last_name: str
    email: str
    password: str

@dataclass
class LoginDTO:
    email: str
    password: str

@dataclass
class UserCreateDTO:
    name: str
    last_name: str
    email: str
    password_hash: str

@dataclass
class UserUpdateDTO:
    name: str
    last_name: str
    email: str

@dataclass
class PermissionCreateDTO:
    name: int
    role: int

@dataclass
class PermissionUpdateDTO:
    name: int
    role: int