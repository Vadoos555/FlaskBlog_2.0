from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from app.config import Config
from flask import redirect, url_for
from app.models import User, Post


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == Config.ADMIN_EMAIL
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login'))


class UserAdmin(AdminModelView):
    form_columns = ['username', 'email', 'posts', 'image_file']
    column_searchable_list = ['username', 'email']
    column_exclude_list = ['password', ]
    column_filters = ['username', 'email']


class PostAdmin(AdminModelView):
    form_columns = ['title', 'content', 'author', 'date_posted']
    column_searchable_list = ['title']
    column_filters = ['title', 'content']
