from app import create_app, db, admin
from app.main.views import UserAdmin, PostAdmin
from app.models import User, Post
from flask import g
from app.config import Config


app = create_app()

admin.add_view(UserAdmin(User, db.session))
admin.add_view(PostAdmin(Post, db.session))


@app.before_request
def before_request():
    g.admin_email = Config.ADMIN_EMAIL

if __name__ == '__main__':
    app.run(debug=True)
    