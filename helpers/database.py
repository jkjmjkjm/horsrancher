#Helper for database. Ensures all database data is sent through one point and locks the data

#TODO find another sql library

from cs50 import SQL
db = SQL("sqlite:///hr-db.db")


def execute(command, *args):
    db.execute('BEGIN TRANSACTION')
    ans = db.execute(command, *args)
    db.execute('COMMIT')
    return ans

def execute_without_freezing(command, *args):
    return db.execute(command, *args)