from fastapi_users import schemas


class UserSchema(schemas.BaseUser[int]):
    id: int
    name: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class ConfigDict:
        from_attributes = True


class UserSchemaAdd(schemas.BaseUserCreate):
    name: str


class UserSchemaEdit(schemas.BaseUserUpdate):
    name: str
