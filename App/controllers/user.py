from App.models import Roster, User
from App.database import db
from App.models import Shift

def create_user(username, password, first_name, last_name):
    newuser = User(username=username, password=password, first_name=first_name, last_name=last_name)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.query(User).filter(User.type == 'user').all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
def clock_in(user_id, shift_id, clock_in_time):
    shift = db.session.get(Shift, shift_id)    
    if not shift or shift.employee_id != user_id:
        return None
    shift.clock_in = clock_in_time
    db.session.commit()
    return True

def clock_out(user_id, shift_id, clock_out_time):
    shift = db.session.get(Shift, shift_id) 
    if not shift or shift.employee_id != user_id:
        print(f'Shift with ID {shift_id} not found for user ID {user_id}.')
        return
    if shift.clock_in is None:
        print(f'Cannot clock out. User {user_id} has not clocked in for shift')
        return
    if shift.clock_out is not None:
        print(f'User {user_id} has already clocked out for shift {shift_id}.')
        return   
    if not shift or shift.employee_id != user_id:
        return None
    shift.clock_out = clock_out_time
    db.session.commit()
    return True

def view_roster(roster_id):
    roster = db.session.get(Roster, roster_id)
    shifts = Shift.query.filter_by(roster_id=roster_id).all()
    if not shifts:
        return (print(f'No shifts found for roster ID {roster_id}'), None)
    for shift in shifts:
        employee = get_user(shift.employee_id)
        employee_name = f'{employee.first_name} {employee.last_name}' if employee else 'Unassigned'
        print(f'Shift ID: {shift.id}, Date: {shift.date}, Start: {shift.start_time}, End: {shift.end_time}, Employee ID: {shift.employee_id}, Name: {employee_name}')