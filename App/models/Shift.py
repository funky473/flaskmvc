from App.database import db

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)

    def __init__(self, name, date, start_time, end_time, employee_id=None):
        self.name = name
        self.start_time = start_time
        self.date = date
        self.employee_id = employee_id
        self.end_time = end_time

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime("%Y-%m-%d"),
            'start_time': self.start_time.strftime("%H:%M:%S"),
            'end_time': self.end_time.strftime("%H:%M:%S")
        }