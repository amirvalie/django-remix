from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.exceptions import ValidationError

class ResizeImage:
    def __init__(self,img_file,format_img="JPEG"):
        valid_format_img=['JPEG','PNG','WEBP']
        self.img_file=img_file
        self.format=format_img.upper() if format_img.upper() in valid_format_img else 'JPEG'

    def set_format_file_name(self):
        return self.format.lower()

    def target_file_name(self,field):
        file_name=self.img_file.name.split('/')[-1].split('.')[0]
        if field == 'thumbnail' or field == 'small':
            file_name=file_name.replace('_cover','')
        #Here we are checking if field name exist at the end of the image file name 
        if not f'_{field}' in file_name:
            return f'{file_name}_{field}'
        return file_name

    def resize_and_reformat(self,size):
        try:
            img=Image.open(self.img_file)
            img.thumbnail(size)
            thumb_bytes=BytesIO()
            img.save(thumb_bytes,format=self.format)
            thumb_file = ContentFile(thumb_bytes.getvalue())
            return thumb_file
        except:
            return self.img_file

    def save(self,target_field,size:tuple):
        thumb_file=self.resize_and_reformat(size)
        file_name=self.target_file_name(target_field.field.name)
        target_field.save(
            f'{file_name}.{self.set_format_file_name()}',
            thumb_file,
            save=False,
        )

