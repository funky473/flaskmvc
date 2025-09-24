from App.database import db

class Roster(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date, nullable=False)
    shifts = db.relationship('Shift', backref='roster', lazy=True)

    def __init__(self, StartDate, EndDate):
        self.StartDate = StartDate
        self.EndDate = EndDate

    def get_json(self):
        return {
            'id': self.id,
            'StartDate': self.StartDate.strftime("%Y-%m-%d"),
            'EndDate': self.EndDate.strftime("%Y-%m-%d")
        }