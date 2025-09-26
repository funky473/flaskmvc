from App.models import Roster,Admin,Shift
from App.database import db


def get_all_rosters():
    return db.session.query(Roster).all()

def get_all_rosters_json():
    rosters = get_all_rosters()
    if not rosters:
        return []
    rosters = [roster.get_json() for roster in rosters]
    return rosters

