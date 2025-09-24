from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.user import User

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
