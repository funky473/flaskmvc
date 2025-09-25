from unicodedata import name
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.user import User
from App.models.Shift import Shift 
from App.models.Roster import Roster

class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, username, password, first_name, last_name):
        super().__init__(username, password, first_name, last_name)

    def get_json(self):
        # Get the base user JSON and add admin-specific fields
        base_json = super().get_json()
        return base_json
    
    def create_roster(self, Start_date, End_date):
        new_roster = Roster(StartDate=Start_date, EndDate=End_date)
        db.session.add(new_roster)
        db.session.commit()
        return new_roster
    
    def create_shift(self, date, start_time, end_time, employee_id,roster_id):
        new_shift = Shift(date=date, start_time=start_time, end_time=end_time, employee_id=employee_id,roster_id=roster_id)
        db.session.add(new_shift)
        db.session.commit()
        return new_shift
