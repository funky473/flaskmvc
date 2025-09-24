from .user import create_user
from .admin import create_admin
from App.database import db

# create_user(username, password, first_name, last_name, isAdmin):
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'Bob', 'Builder')
    create_admin('admin', 'adminpass', 'Admin', 'User')
