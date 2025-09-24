from App.database import db

class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), nullable=False)
   # shifts = db.relationship('Shift', backref='roster', lazy=True)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime("%Y-%m-%d")
        }