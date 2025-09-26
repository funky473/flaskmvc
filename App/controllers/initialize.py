from .user import create_user
from .admin import create_admin, create_shift
from App.database import db
from datetime import date, timedelta
from App.models.Roster import Roster

def initialize():
    db.drop_all()
    db.create_all()
    
    # Create admin users
    admin1 = create_admin('admin1', 'admin1pass', 'John', 'Smith')
    admin2 = create_admin('admin2', 'admin2pass', 'Sarah', 'Johnson')
    admin3 = create_admin('admin3', 'admin3pass', 'Michael', 'Brown')
    admin4 = create_admin('admin4', 'admin4pass', 'Emily', 'Davis')
    admin5 = create_admin('admin5', 'admin5pass', 'David', 'Wilson')
    
    # Create regular users
    user1 = create_user('user1', 'pass1', 'James', 'Anderson')
    user2 = create_user('user2', 'pass2', 'Lisa', 'Taylor')
    user3 = create_user('user3', 'pass3', 'Robert', 'Martinez')
    user4 = create_user('user4', 'pass4', 'Amy', 'Garcia')
    user5 = create_user('user5', 'pass5', 'William', 'Lee')
    
    # Create rosters directly
    current_date = date(2025, 9, 25)  # Using the current date from context
    
    # Create roster objects directly
    roster1 = Roster(StartDate=current_date, EndDate=current_date + timedelta(days=7))
    roster2 = Roster(StartDate=current_date + timedelta(days=8), EndDate=current_date + timedelta(days=14))
    db.session.add(roster1)
    db.session.add(roster2)
    db.session.commit()
    
    # Create shifts for roster1 (5 shifts)
    create_shift(admin1.id, current_date, "09:00", "17:00", user1.id, roster1.id)
    create_shift(admin1.id, current_date, "10:00", "18:00", user2.id, roster1.id)
    create_shift(admin1.id, current_date + timedelta(days=1), "09:00", "17:00", user3.id, roster1.id)
    create_shift(admin1.id, current_date + timedelta(days=1), "10:00", "18:00", user4.id, roster1.id)
    create_shift(admin1.id, current_date + timedelta(days=2), "09:00", "17:00", user5.id, roster1.id)
    
    # Create shifts for roster2 (5 shifts)
    next_week = current_date + timedelta(days=8)
    create_shift(admin2.id, next_week, "09:00", "17:00", user1.id, roster2.id)
    create_shift(admin2.id, next_week, "10:00", "18:00", user2.id, roster2.id)
    create_shift(admin2.id, next_week + timedelta(days=1), "09:00", "17:00", user3.id, roster2.id)
    create_shift(admin2.id, next_week + timedelta(days=1), "10:00", "18:00", user4.id, roster2.id)
    create_shift(admin2.id, next_week + timedelta(days=2), "09:00", "17:00", user5.id, roster2.id)
