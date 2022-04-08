from typing import List
from PIL import Image
from PIL.ExifTags import TAGS

import climage
from sqlalchemy.orm import Session

from src.db.db import engine
from src.db.model import Image


def exif_info(image_path):
    """
    Returns a dictionary of exif data of an image file.
    """
    ret = {}
    image = Image.open(image_path)
    image.verify()
    exifdata = image._getexif()
    for tag_id, data in exifdata.items():
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)

        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        ret[TAGS.get(tag_id, tag_id)] = data
    return ret

def cli_print(image_path):
    output = climage.convert(image_path, is_unicode=True,width=32)
    return output

def get_all_images() -> List[Image]:
    with Session(engine) as session:
        return session.query(Image).all()


def save_bitmap(image, bitmap):
    with Session(engine, expire_on_commit=False) as session:
        image.notes = bitmap
        session.add(image)
        session.commit()
    return True

