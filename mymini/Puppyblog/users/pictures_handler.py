from PIL import Image
from flask import current_app
import os




def add_picture(pic_upload, username):
  filename = pic_upload.filename
  exc = filename.split('.')[-1]
  
  storage_name = str(username) + "." +exc
  
  path = os.path.join(current_app.root_path, 'static/profile_pics', storage_name)
  
  file_size = (200, 200)
  
  pic = Image.open(pic_upload)
  pic.thumbnail(file_size)
  pic.save(path)
  
  return storage_name