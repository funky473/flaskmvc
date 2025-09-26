from App.models import Admin, Shift, Roster
from App.controllers.user import get_user
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

def create_roster(admin_id,Start_date, End_date):
    admin = Admin.query.get(admin_id)
    if not admin:
        return None
    new_roster = admin.create_roster(Start_date,End_date)
    db.session.add(new_roster)
    db.session.commit()
    return new_roster

def create_shift(admin_id, date, start_time, end_time, employee_id, roster_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return None
    new_shift = Shift(date=date, start_time=start_time, end_time=end_time, employee_id=employee_id, roster_id=roster_id)
    db.session.add(new_shift)
    db.session.commit()
    return new_shift

def ViewReport(roster_id):
    roster = db.session.get(Roster, roster_id)
    shifts = Shift.query.filter_by(roster_id=roster_id).all()
    if not shifts:
        return (print(f'No shifts found for roster ID {roster_id}'), None)
    print(f'Roster ID: {roster.id}, Start Date: {roster.StartDate}, End Date: {roster.EndDate}')
    for shift in shifts:
        employee = get_user(shift.employee_id)
        employee_name = f'{employee.first_name} {employee.last_name}' if employee else 'Unassigned'
        print(f'Shift ID: {shift.id}, Date: {shift.date}, Start: {shift.start_time}, End: {shift.end_time}, Employee ID: {shift.employee_id}, Name: {employee_name}, Clock In: {shift.clock_in}, Clock Out: {shift.clock_out}')
    return roster