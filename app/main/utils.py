import os, secrets
from flask import current_app
from PIL import Image

def save_picture(form_picture, image_type):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension

    return_value = {'filename': picture_filename, 'orientation': None}

    if image_type == 'profile_picture':
        picture_path = os.path.join(current_app.root_path, 'static/images/profile_pictures', picture_filename)
        output_size = (250, 250) 
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        return return_value

        
    elif image_type == 'artwork':
        picture_path = os.path.join(current_app.root_path, 'static/images/artwork', picture_filename)
        i = Image.open(form_picture)
        width, height = i.size
        if width > height:
            return_value['orientation'] = 'landscape'
            output_size = (512, 364)
            i.thumbnail(output_size)
            i.save(picture_path)
            return return_value
        elif height > width:
            return_value['orientation'] = 'portrait'
            output_size = (364,512)
            i.thumbnail(output_size)
            i.save(picture_path)
            return return_value
        else:
            return_value['orientation'] = 'square'
            output_size = (500, 500)
            i.thumbnail(output_size)
            i.save(picture_path)
            return return_value
