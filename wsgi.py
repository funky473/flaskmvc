import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.controllers.admin import create_admin, get_all_admins
from App.database import db, get_migrate
from App.models import User
from App.models import Admin
from App.main import create_app
from App.models.Shift import Shift
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, get_user )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("first_name", default="Rob")
@click.argument("last_name", default="Builder")
def create_user_command(username, password, first_name, last_name):
    create_user(username, password, first_name, last_name)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        users = get_all_users()
        for user in users:
            print(user.username)
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

admin_cli = AppGroup('admin', help='Admin object commands')
@admin_cli.command("create", help="Creates an admin")
@click.argument("username", default="2dmin")
@click.argument("password", default="2dminpass")
@click.argument("first_name", default="2dmin")
@click.argument("last_name", default="User")
def create_admin_command(username, password, first_name, last_name):
    create_admin(username, password, first_name, last_name)
    print(f'Admin {username} created!')

@admin_cli.command("list", help="Lists admins in the database")
def list_admin_command():
    admins = get_all_admins()
    for admin in admins:
        print(admin.username)

app.cli.add_command(admin_cli)
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

# this command will be to create a shift
# flask shift create 2023-10-10 09:00:00 17:00:00
# flask shift list json
shift_cli = AppGroup('shift', help='Shift object commands')

@shift_cli.command("create", help="Creates a shift")
def create_shift_command():
    date = click.prompt('Enter date (YYYY-MM-DD)', type=str)
    start_time = click.prompt('Enter start time (HH:MM:SS)', type=str)
    end_time = click.prompt('Enter end time (HH:MM:SS)', type=str)
    if click.confirm('Do you want to assign an employee?'):
        employee_id = click.prompt('Enter employee ID', type=int)
    else:
        employee_id = None
    
    create_shift(date, start_time, end_time, employee_id)
    print(f'Shift created for {date} from {start_time} to {end_time} for employee {employee_id}')

@shift_cli.command("list", help="Lists shifts in the database")
@click.argument("format", default="string")
def list_shift_command(format):
    if format == 'string':
        print(get_all_shifts())
    else:
        print(get_all_shifts_json())

app.cli.add_command(shift_cli)