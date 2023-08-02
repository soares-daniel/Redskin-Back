import os

from fastapi import UploadFile

from app.repositories.base import BaseRepository
from app.config.manager import settings


class AssetsRepository(BaseRepository):
    """Assets repository"""
    @staticmethod
    async def upload_profile_pic(user_id: int, file: UploadFile) -> str:
        """Upload new profile picture for current user"""

        # Directory Creation: Ensuring the directory exists
        directory = f"{settings.ASSETS_PATH}/{str(user_id)}"
        os.makedirs(directory, exist_ok=True)

        # Move file to static assets directory
        file_location = f"{directory}/{file.filename}"

        # Error Handling: Handling potential errors in file I/O
        try:
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
            file.file.close()  # Clearing the temporary file
        except Exception as e:
            raise IOError("Failed to save the image.") from e

        return file_location
