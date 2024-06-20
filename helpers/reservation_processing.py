from helpers.database import db
import datetime
import os
import json
from random import randint
import helpers.database
from helpers.social import getcenterphone, getcenterphoneform
from flask import session
#from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import sendgrid

sendgrid_client = sendgrid.SendGridAPIClient("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")

available_res_codes = ['2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def process_reservation(centerID, levelID, instructorID, horseID, day, month, year, hour, mins, contact_info):
    #1. Is valid date?
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        return 'Wrong date', False
    #2. Is valid time?
    if int(hour) > 24 or int(hour) < 0 or int(mins) > 59 or int(mins) < 0:
        return 'Wrong time', False
    #2,3. Center exists?
    center = helpers.database.execute_without_freezing('SELECT * FROM center WHERE id = ?', centerID)
    if len(center) != 1:
        return 'Bad center', False
    center = center[0]
    #2,6 Is part of center's timetable?
    center_offering = helpers.database.execute_without_freezing('SELECT * FROM center_offering WHERE center_id = ?', centerID)[0]
    form_time = int(hour)*60+int(mins)
    if not form_time in range(center_offering['center_starts_classes'], center_offering['center_ends_classes']+1, center_offering['classes_every']):
        return 'Bad time', False
    #3. level exists and in center?
    level = helpers.database.execute_without_freezing('SELECT * FROM level WHERE centerID = ? AND ID = ?', centerID, levelID)
    if len(level) != 1:
        return 'Bad level', False
    else:
        level = level[0]
    #4. Horse exists and in level?
    horse = helpers.database.execute_without_freezing('SELECT * FROM horse WHERE levelID = ? AND ID = ?', levelID, horseID)
    if len(horse) != 1:
        return 'Bad horse', False
    else:
        horse = horse[0]
    #5. Instructor exists and in level?
    instructor = helpers.database.execute_without_freezing('SELECT * FROM instructor WHERE levelID = ? AND ID = ?', levelID, instructorID)
    if len(instructor) != 1:
        return 'Bad instructor', False
    else:
        instructor = instructor[0]
    #6. Freeze database
    db.execute('BEGIN TRANSACTION')
    #7. Is instructor available?
    if not db.execute("SELECT COUNT(*) FROM reservation WHERE instructor_id = ? AND day = ? AND month = ? AND year = ? AND start_time = ?", instructorID, int(day), int(month), int(year), form_time)[0]['COUNT(*)'] < center_offering['class_size']:
        db.execute('COMMIT')
        return 'Unavailable instructor', False
    #8. Is horse available?
    if not db.execute("SELECT COUNT(*) FROM reservation WHERE horse_id = ? AND day = ? AND month = ? AND year = ? AND start_time = ?", horseID, int(day), int(month), int(year), form_time)[0]['COUNT(*)'] < 1:
        db.execute('COMMIT')
        return 'Unavailable horse', False
    #8,5. Generate and check reservation code
    res_code = ''
    while True:
        res_code = ''
        for i in range(8):
            res_code = res_code + available_res_codes[randint(0, len(available_res_codes)-1)]
        if not len(db.execute('SELECT * FROM reservation WHERE reservation_code = ?', res_code)) > 0:
            break
    #9. Add to database
    db.execute('INSERT INTO reservation(center_id, level_id, horse_id, instructor_id, start_time, length, day, month, year, reservation_code, email, name, phone) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', 
    centerID, levelID, horseID, instructorID, form_time, center_offering['classes_length'], int(day), int(month), int(year), res_code, contact_info['email'], contact_info['name'], contact_info['phone'])
    #10. Unfreeze database
    db.execute('COMMIT')
    #11. Send mail
    message = Mail(
        from_email='reservations@horsrancher.com',
        to_emails=[contact_info['email']])
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = {
        "res_code":res_code,
        "center_name":center['displayName'],
        "short_description":center['short_description'],
        "center_id":center['ID'],
        "main_photo":center['bannerLoc'],
        "date":str(day)+'/'+str(month)+'/'+str(year),
        "time":str(hour)+':'+str(mins),
        "level":level['levelName'],
        "horse":horse['Name'],
        "horse_pic":horse['pictureURL'],
        "instructor":instructor['Name'],
        "instructor_pic":instructor['pictureURL'],
        "reserver_name":contact_info['name'],
        "reserver_email":contact_info['email'],
        "reserver_phone":contact_info['form_phone'],
        "formatted_place_phone":getcenterphoneform(centerID),
        "unformatted_place_phone": getcenterphone(centerID)
    }
    message.template_id = 'd-31ab28fd49694c26a8c28826f4acd699'
    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        response = sendgrid_client.send(message)
    except Exception as e:
        print("Error: {0}".format(e))
    #return str(response.status_code)
    return 'Success', True

def update_instructor(instructor_id, name, picture, levelID):
    prev_info = helpers.database.execute_without_freezing('SELECT * FROM instructor WHERE ID = ? AND centerID = ?', instructor_id, session.get('center_id_auth'))
    if picture not in os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/instructors/') and picture != "../../../assets/etc/missing-profile.png":
        return False
    if len(helpers.database.execute_without_freezing('SELECT * FROM level WHERE ID = ? AND centerID = ?', levelID, session['center_id_auth'])) != 1:
        return False
    if len(name) < 1 or len(name) > 50:
        return False
    if len(prev_info) != 1:
        if instructor_id == '+':
            helpers.database.execute('INSERT INTO instructor(Name, pictureURL, levelID, centerID) VALUES(?,?,?,?)', name, picture, levelID, session.get('center_id_auth'))
        else:
            return False
    helpers.database.execute("UPDATE instructor SET Name=?, pictureURL=?, levelID=? WHERE ID=?", name, picture, levelID, instructor_id)

def delete_instructor(instructor_id):
    prev_info = helpers.database.execute_without_freezing('SELECT * FROM instructor WHERE ID = ? AND centerID = ?', instructor_id, session.get('center_id_auth'))
    if len(prev_info) != 1:
            return False
    helpers.database.execute("DELETE FROM instructor WHERE ID=?", instructor_id)

def update_horse(horse_id, name, picture, levelID):
    prev_info = helpers.database.execute_without_freezing('SELECT * FROM horse WHERE ID = ? AND centerID = ?', horse_id, session.get('center_id_auth'))
    if picture not in os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/horses/') and picture != "../../../assets/etc/missing-profile.png":
        return False
    if len(helpers.database.execute_without_freezing('SELECT * FROM level WHERE ID = ? AND centerID = ?', levelID, session['center_id_auth'])) != 1:
        return False
    if len(name) < 1 or len(name) > 50:
        return False
    if len(prev_info) != 1:
        if horse_id == '+':
            helpers.database.execute('INSERT INTO horse(Name, pictureURL, levelID, centerID) VALUES(?,?,?,?)', name, picture, levelID, session.get('center_id_auth'))
        else:
            return False
    helpers.database.execute("UPDATE horse SET Name=?, pictureURL=?, levelID=? WHERE ID=?", name, picture, levelID, horse_id)

def delete_horse(horse_id):
    prev_info = helpers.database.execute_without_freezing('SELECT * FROM horse WHERE ID = ? AND centerID = ?', horse_id, session.get('center_id_auth'))
    if len(prev_info) != 1:
            return False
    helpers.database.execute("DELETE FROM horse WHERE ID=?", horse_id)

def update_level(level_id, name, euros):
    prev_info = helpers.database.execute_without_freezing('SELECT * FROM level WHERE ID = ? AND centerID = ?', level_id, session.get('center_id_auth'))
    if len(name) < 1 or len(name) > 50:
        return False
    if len(prev_info) != 1:
        if level_id == '+':
            helpers.database.execute('INSERT INTO level(levelName, centerID, EUR_hour) VALUES(?,?,?)', name, session.get('center_id_auth'), abs(float(euros)))
        else:
            return False
    helpers.database.execute("UPDATE level SET levelName=?, EUR_hour=? WHERE ID=?", name, abs(float(euros)), level_id)

def delete_level(level_id):
    prev_info = helpers.database.execute_without_freezing('SELECT * FROM level WHERE ID = ? AND centerID = ?', level_id, session.get('center_id_auth'))
    if len(prev_info) != 1:
        return False
    helpers.database.execute("DELETE FROM level WHERE ID=?", level_id)