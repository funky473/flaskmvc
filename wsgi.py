import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from datetime import datetime
from App.controllers.admin import create_admin, get_all_admins,get_admin,create_roster,create_shift,ViewReport
from App.controllers.roster import get_all_rosters
from App.controllers.shift import get_all_shifts, get_all_shifts_json, validate_shift
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, get_user,clock_in,clock_out,view_roster)

from App.database import db, get_migrate
from App.models import User
from App.models import Admin
from App.main import create_app
from App.models.Shift import Shift

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
    print('ID : First Name : Last Name')
    if format == 'string':
        users = get_all_users()
        for user in users:
            print(user.id, user.first_name, user.last_name)
    else:
        print(get_all_users_json())


#clock in command
@user_cli.command("clockin", help="Clock in a user")
def clockin_user_command():
    print('List of employees:')
    employees = get_all_users()
    for emp in employees:
        print(f'ID: {emp.id}, Name: {emp.first_name} {emp.last_name}')
    user_id = click.prompt('Enter employee ID to clock in', type=int)
    user = get_user(user_id)
    if not user:
        print(f'User with ID {user_id} not found.')
        return
    
    shifts = [shift for shift in get_all_shifts() if shift.employee_id == user_id]
    if not shifts:
        print(f'No shifts found for user ID {user_id}')
        return
    
    for shift in shifts:
        print(f'Shift ID: {shift.id}, Date: {shift.date}, Start Time: {shift.start_time}, End Time: {shift.end_time}, Employee ID: {shift.employee_id}, Clock In: {shift.clock_in}, Clock Out: {shift.clock_out}')
    
    shift_id = click.prompt('Enter Shift ID to clock in', type=int)
    shift = db.session.get(Shift, shift_id)
    if not shift or shift.employee_id != user_id:
        print(f'Shift with ID {shift_id} not found for user ID {user_id}.')
        return
    if shift.clock_in is not None:
        print(f'User {user_id} has already clocked in for shift {shift_id}.')
        return

    clock_in_time = click.prompt('Enter clock-in time (HH:MM)', type=str)
    # Validate time format
    try:
        datetime.strptime(clock_in_time, '%H:%M')
    except ValueError:
        print('Invalid time format. Please use HH:MM')
        return
    
    try:
        # Call the user's clock_in method with shift_id (not shift object)
        if clock_in(user_id, shift_id, clock_in_time) is True:
            print(f'User {user_id} clocked in at {clock_in_time}.')
    except Exception as e:
        print(f'Error clocking in: {str(e)}')

@user_cli.command("clockout", help="Clock out a user")
def clockout_user_command():
    print('List of employees:')
    employees = get_all_users()
    for emp in employees:
        print(f'ID: {emp.id}, Name: {emp.first_name} {emp.last_name}')
    user_id = click.prompt('Enter employee ID to clock out', type=int)
    user = get_user(user_id)
    if not user:
        print(f'User with ID {user_id} not found.')
        return
    
    shifts = [shift for shift in get_all_shifts() if shift.employee_id == user_id]
    if not shifts:
        print(f'No shifts found for user ID {user_id}')
        return
    
    for shift in shifts:
        print(f'Shift ID: {shift.id}, Date: {shift.date}, Start Time: {shift.start_time}, End Time: {shift.end_time}, Employee ID: {shift.employee_id}, Clock In: {shift.clock_in}, Clock Out: {shift.clock_out}')
    
    shift_id = click.prompt('Enter Shift ID to clock out', type=int)

    clock_out_time = click.prompt('Enter clock-out time (HH:MM)', type=str)
    # Validate time format
    try:
        datetime.strptime(clock_out_time, '%H:%M')
    except ValueError:
        print('Invalid time format. Please use HH:MM')
        return
    
    try:
        if clock_out(user_id, shift_id, clock_out_time) is True:
            print(f'User {user_id} clocked out at {clock_out_time}.')
    except Exception as e:
        print(f'Error clocking out: {str(e)}')


@user_cli.command("viewroster", help="View Roster for a user")
def viewroster_user_command():
    rosters = get_all_rosters()
    if not rosters:
        print('No rosters found.')
        return
    print('List of rosters:')
    for roster in rosters:
        print(f'ID: {roster.id}, Start Date: {roster.StartDate}, End Date: {roster.EndDate}')
    roster_id = click.prompt('Enter Roster ID to view shifts', type=int)
    view_roster(roster_id)
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
    print('ID : First Name : Last Name')
    admins = get_all_admins()
    for admin in admins:
        print(admin.id, admin.first_name, admin.last_name)

@admin_cli.command("newroster", help="Creates a roster")
def create_roster_command():
    print('Creating a new roster:')
    print('select an admin to create the roster:')
    admins = get_all_admins()
    for admin in admins:
        print(f'ID: {admin.id}, Name: {admin.first_name} {admin.last_name}')
    admin_id = click.prompt('Enter admin ID', type=int)

    start_date = click.prompt('Enter start date (YYYY-MM-DD)', type=str)
    end_date = click.prompt('Enter end date (YYYY-MM-DD)', type=str)
    
    # Convert string dates to Python date objects
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    #checking to see if there is a shift in the database like this
    create_roster(admin_id, start_date_obj, end_date_obj)
    print(f'Roster created from {start_date} to {end_date}')

@admin_cli.command("newshift", help="Creates a shift")
def create_shift_command():
    print('Creating a new shift:')
    print('select an admin to create the shift:')
    admins = get_all_admins()
    for admin in admins:
        print(f'ID: {admin.id}, Name: {admin.first_name} {admin.last_name}')
    admin_id = click.prompt('Enter admin ID', type=int)
    admin = get_admin(admin_id)
    if not admin:
        print(f'Admin with ID {admin_id} not found.')
        return

    date = click.prompt('Enter date (YYYY-MM-DD)', type=str)
    start_time = click.prompt('Enter start time (HH:MM)', type=str)
    end_time = click.prompt('Enter end time (HH:MM)', type=str)

    # Convert string date to Python date object
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    
    # Keep times as strings since SQLite doesn't support time objects
    # Just validate the format
    try:
        datetime.strptime(start_time, '%H:%M')
        datetime.strptime(end_time, '%H:%M')
    except ValueError:
        print('Invalid time format. Please use HH:MM')
        return

    print('Please select Roster ID from the following list:')
    rosters = get_all_rosters()
    if not rosters:
        print('No rosters found. Please create a roster first.')
        return
    for roster in rosters:
        print(f'ID: {roster.id}, Start Date: {roster.StartDate}, End Date: {roster.EndDate}')
    roster_id = click.prompt('Enter Roster ID to assign the shift', type=int)
    
    print('List of employees:')
    employees = get_all_users()
    for emp in employees:
        print(f'ID: {emp.id}, Name: {emp.first_name} {emp.last_name}')
    employee_id = click.prompt('Enter employee ID to assign the shift', type=int)
    if not get_user(employee_id):
        print(f'User with ID {employee_id} not found.')
        return
    # Pass the time values as strings
    create_shift(admin_id,date_obj, start_time, end_time, employee_id, roster_id)
    print(f'Shift created on {date_obj} from {start_time} to {end_time} for employee {employee_id}')

@admin_cli.command("viewreport", help="View Report for a roster")
def viewreport_admin_command():
    rosters = get_all_rosters()
    if not rosters:
        print('No rosters found.')
        return
    print('List of rosters:')
    for roster in rosters:
        print(f'ID: {roster.id}, Start Date: {roster.StartDate}, End Date: {roster.EndDate}')
    roster_id = click.prompt('Enter Roster ID to view report', type=int)
    ViewReport(roster_id)

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

@shift_cli.command("list", help="Lists shifts in the database")
@click.argument("format", default="string")
def list_shift_command(format):
    if format == 'string':
        for shift in get_all_shifts():
            employee = get_user(shift.employee_id)
            employee_name = employee.first_name + ' ' + employee.last_name
            print(f' Date: {shift.date}, Start Time: {shift.start_time}, End Time: {shift.end_time}, Roster ID: {shift.roster_id}')
            print(f'  Assigned to Employee ID: {shift.employee_id}, Name: {employee_name}, Clock In: {shift.clock_in}, Clock Out: {shift.clock_out}')
    else:
        print(get_all_shifts_json())

app.cli.add_command(shift_cli)

roster_cli = AppGroup('roster', help='Roster object commands')

@roster_cli.command("list", help="Lists rosters in the database")
@click.argument("format", default="string")
def list_roster_command(format):
    if format == 'string':
        for roster in get_all_rosters():
            print(f'ID: {roster.id}, Start Date: {roster.StartDate}, End Date: {roster.EndDate}')
        print("to see all the shift from that roster, enter the roster ID below")
        roster_id = click.prompt('Enter roster ID', type=int)
        shifts = [shift for shift in get_all_shifts() if shift.roster_id == roster_id]
        if not shifts:
            print(f'No shifts found for roster ID {roster_id}')
            return
        for shift in shifts:
            print(f'Shift ID: {shift.id}, Date: {shift.date}, Start Time: {shift.start_time}, End Time: {shift.end_time}, Employee ID: {shift.employee_id}')

app.cli.add_command(roster_cli)