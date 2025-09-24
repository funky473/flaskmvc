from App.models import Admin
from App.database import db


def create_admin(username, password, first_name, last_name):
    newadmin = Admin(username=username, password=password, first_name=first_name, last_name=last_name)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def get_all_admins():
    return db.session.query(Admin).all()