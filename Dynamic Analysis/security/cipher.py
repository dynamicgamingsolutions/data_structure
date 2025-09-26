from PIL import Image
from PIL.ExifTags import TAGS
import chardet

def get_user_comment(imagename):
    image = Image.open(imagename)

    # Extract the EXIF data
    exif_data = image._getexif()

    # If the image has EXIF data
    if exif_data is not None:
        # Iterate over all EXIF tags
        for tag_id in exif_data:
            # Get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                encoding = chardet.detect(data)['encoding']
                data = data.decode(encoding, errors='ignore')
            # If the tag is 'UserComment', return the last 128 characters
            if tag == 'UserComment':
                return data[-128:]
            
# print(get_user_comment('C:\\Users\\Paul Collins\\Dynamic Analysis\\security\\The Man - The Myth - The Ray.jpg'))