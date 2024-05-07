import sqlalchemy as sa
import sqlalchemy.orm as so

from datetime import datetime
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedSerializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(25), unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(85), unique=True, nullable=False)
    image_file: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False, default='default.jpg')
    password: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    
    posts: so.Mapped[list["Post"]] = so.relationship(back_populates='author', lazy=True)
    
    def get_reset_token(self, expires_sec=600):
        s = TimedSerializer(current_app.config['SECRET_KEY'], salt='reset-password')
        return s.dumps({'user_id': str(self.id)})
    
    @staticmethod
    def verify_reset_token(token):
        s = TimedSerializer(current_app.config['SECRET_KEY'], salt='reset-password')
        try:
            user_id = s.loads(token)['user_id']
        except Exception as err:
            print(f'error of extract token: {err}')
            return None
        return User.query.get(int(user_id))
    
    def __repr__(self) -> str:
        return f'User({self.username}, {self.email}, {self.image_file})'


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    date_posted: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False, default=datetime.now)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    
    def __repr__(self) -> str:
        return f'Post({self.title}, {self.date_posted})'