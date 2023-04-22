from pathlib import Path
import uuid

from fastapi import UploadFile


def get_user_avatar_path(username: str) -> str:
    return f"users/{username}/avatar"


def save_user_image(image: UploadFile, filename: str, username: str) -> None:
    file_location = Path("files/" + get_user_avatar_path(username))
    file_location.mkdir(parents=True, exist_ok=True)
    with open(file_location / filename, "wb+") as file_object:
        file_object.write(image.file.read())


def get_user_image_filename(image: UploadFile | None) -> str | None:
    if not image:
        return None
    filename = f"{image.filename if image.filename else uuid.uuid4()}"
    return filename
