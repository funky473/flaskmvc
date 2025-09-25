from App.models import Roster,Admin,Shift
from App.database import db

def create_shift(admin_id, date, start_time, end_time, employee_id, roster_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return None
    new_shift = admin.create_shift(date, start_time, end_time, employee_id, roster_id)
    db.session.add(new_shift)
    db.session.commit()
    return new_shift

def get_all_shifts():
    return db.session.query(Shift).all()

def get_all_shifts_json():
    shifts = get_all_shifts()
    if not shifts:
        return []
    shifts = [shift.get_json() for shift in shifts]
    return shifts

def validate_shift(shift):
    #ensure that one employee has one shift for one date
    existing_shift = db.session.execute(
        db.select(Shift).filter_by(employee_id=shift.employee_id, date=shift.date)
    ).scalars().first()
    double_shift = db.session.execute(
        db.select(Shift).filter_by(date=shift.date, start_time=shift.start_time, end_time=shift.end_time)
    ).scalars().first()
    if existing_shift or double_shift:
        return False
    return True
