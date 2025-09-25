from App.models import Admin
from App.database import db


def create_admin(username, password, first_name, last_name):
    newadmin = Admin(username=username, password=password, first_name=first_name, last_name=last_name)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def get_all_admins():
    return db.session.query(Admin).all()

def get_admin(id):
    return db.session.get(Admin, id)

def create_roster(admin_id, Start_date, End_date):
    admin = get_admin(admin_id)
    if admin:
        return admin.create_roster(Start_date, End_date)
    return None

def create_shift(admin_id, date, start_time, end_time, employee_id=None):
    admin = get_admin(admin_id)
    if admin:
        return admin.create_shift(date, start_time, end_time, employee_id)
    return None
