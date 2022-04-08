from PIL import Image
from PIL.ExifTags import TAGS


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
