from App.models import Roster,Admin
from App.database import db

def create_roster(admin_id,Start_date, End_date):
    admin = Admin.query.get(admin_id)
    if not admin:
        return None
    new_roster = admin.create_roster(Start_date,End_date)
    db.session.add(new_roster)
    db.session.commit()
    return new_roster

def get_all_rosters():
    return db.session.query(Roster).all()

def get_all_rosters_json():
    rosters = get_all_rosters()
    if not rosters:
        return []
    rosters = [roster.get_json() for roster in rosters]
    return rosters