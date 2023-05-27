import pydantic
from fastapi import APIRouter, status

from app.models.schemas.user import UserInCreate, UserInResponse, UserInUpdate
from app.repositories.user import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    path="",
    response_model=list[UserInResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users():
    """Get all users"""
    raise NotImplementedError

@router.get(
    path="/{user_id}",
    response_model=UserInResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: int):
    """Get user by id"""
    raise NotImplementedError

@router.post(
    path="",
    response_model=UserInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserInCreate):
    """Create user"""
    raise NotImplementedError

@router.put(
    path="/{user_id}",
    response_model=UserInResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(user_id: int, user: UserInUpdate):
    """Update user"""
    raise NotImplementedError
