import secrets
import os
from PIL import Image
from flask import url_for, current_app
from app import mail
from app.models import User
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_foto', picture_fn)
    
    output_size = (150, 150)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fn


def send_reset_email(user:User):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request',
                  sender='noreply@blog.com',
                  recipients=[user.email])
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    