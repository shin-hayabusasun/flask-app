from webapp import app,db
from webapp import Post,User


with app.app_context():
    db.create_all()