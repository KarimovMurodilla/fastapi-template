from typing import Annotated

from fastapi import Depends

from api.auth_user import User, current_user
from utils.unitofwork import IUnitOfWork, UnitOfWork

uow = UnitOfWork
UOWDep = Annotated[IUnitOfWork, Depends(uow)]
CurrentUser = Annotated[User, Depends(current_user)]
