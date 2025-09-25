from App.database import db

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    clock_in = db.Column(db.String, nullable=True)
    clock_out = db.Column(db.String, nullable=True)
    roster_id = db.Column(db.Integer, db.ForeignKey('roster.id'), nullable=True)  # Add this line

    def __init__(self, date, start_time, end_time, employee_id, roster_id,clock_in=None, clock_out=None):
        self.start_time = start_time
        self.date = date
        self.end_time = end_time
        self.employee_id = employee_id
        self.roster_id = roster_id
        self.clock_in = clock_in
        self.clock_out = clock_out

    def get_json(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.strftime("%Y-%m-%d"),
            'start_time': self.start_time.strftime("%H:%M:%S"),
            'end_time': self.end_time.strftime("%H:%M:%S"),

        }