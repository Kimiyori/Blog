from io import BytesIO
from pathlib import Path
import uuid
import shutil
from fastapi import UploadFile


def get_user_avatar_path(username: str) -> str:
    return f"users/{username}/avatar"


def save_user_image(image: UploadFile, filename: str, username: str) -> None:
    # exception handler
    def handler(func, path, exc_info) -> None:  # type: ignore
        print(exc_info)

    file_location = Path("files/" + get_user_avatar_path(username))
    shutil.rmtree(file_location, onerror=handler)
    file_location.mkdir(parents=True, exist_ok=True)
    with open(file_location / filename, "wb") as file_object:
        file_object.write(image)


def get_user_image_filename(image: UploadFile | None) -> str | None:
    filename = f"{uuid.uuid4()}.jpg"
    return filename
