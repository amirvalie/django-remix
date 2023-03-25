from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.exceptions import ValidationError

class ResizeImage:
    def __init__(self,img_file,format_img="JPEG"):
        valid_format_img=['JPEG','PNG','WEBP']
        self.img_file=img_file
        self.format=format_img.upper() if format_img.upper() in valid_format_img else 'JPEG'
        self.target_file_name=self.img_file.name.split('/')[-1].split('.')[0]

    def set_format_file_name(self):
        return self.format.lower()

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

    def save_cover(self,target_field,size:tuple):
        thumb_file=self.resize_and_reformat(size)
        target_field.save(
            f'{self.target_file_name}_cover.{self.set_format_file_name()}',
            thumb_file,save=False
        )

    def save_thumbnail(self,target_field,size:tuple):
        thumb_file=self.resize_and_reformat(size)
        target_field.save(
            f'{self.target_file_name}_thumb.{self.set_format_file_name()}',
            thumb_file,save=False
        )

    def save_small(self,target_field,size:tuple):
        thumb_file=self.resize_and_reformat(size)
        target_field.save(
            f'{self.target_file_name}_small.{self.set_format_file_name()}',
            thumb_file,save=False
        )
