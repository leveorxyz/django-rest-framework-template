import base64
from datetime import datetime, timezone

from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename, slugify
from django.db import models


def generate_file_and_name(image_data: str, user_id: int):
    """
    This method is used to generate a file name for the profile photo.
    """
    current_timestamp = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H_%M_%S_%f")
    mimetype, data = image_data.split(";base64,")
    file_extention = mimetype.split("/")[-1]
    image_name = get_valid_filename(f"{user_id}_{current_timestamp}.{file_extention}")
    image_file = ContentFile(base64.b64decode(data), name=image_name)
    return image_name, image_file
