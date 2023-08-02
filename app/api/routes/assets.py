import fastapi
from fastapi import UploadFile

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.repository import get_repository
from app.models.db.user import User
from app.repositories.assets import AssetsRepository
from app.repositories.user import UserRepository

router = fastapi.APIRouter(prefix="/assets", tags=["assets"])


@router.post(
    path="/upload/profile_pic",
    response_model=str,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def upload_profile_pic(
        assets_repo: AssetsRepository = fastapi.Depends(get_repository(repo_type=AssetsRepository)),
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        current_user: User = fastapi.Depends(get_current_user),
        file: UploadFile = fastapi.File(...),
) -> str:
    """Upload new profile picture for current user"""
    allowed_file_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_file_types:
        raise fastapi.HTTPException(
            status_code=415,
            detail=f"Allowed types: {allowed_file_types}",
        )
    try:
        file_path = await assets_repo.upload_profile_pic(current_user.id, file)
    except ValueError as ve:
        raise fastapi.HTTPException(status_code=400, detail=str(ve))
    except IOError as ioe:
        raise fastapi.HTTPException(status_code=500, detail=str(ioe))

    updated_user = await user_repo.update_user_profile_pic(user_id=current_user.id, profile_pic=file_path)

    if not updated_user:
        raise fastapi.HTTPException(status_code=500, detail="Failed to update user profile pic")

    return file_path
