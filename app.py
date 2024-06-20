# HorsRancher Flask Backend Code

#Imports required
from flask import Flask, request, redirect, g, url_for, session, send_file, render_template
import helpers
from tempfile import mkdtemp
from flask_session import Session
from werkzeug.exceptions import default_exceptions
from werkzeug.utils import secure_filename
import sys
import os
import json
from time import sleep
import urllib

#Preparation
app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.jinja_env.filters['timeformat'] = helpers.minstohhmm
app.jinja_env.filters['hours'] = helpers.converttohours
app.jinja_env.filters['mins'] = helpers.converttominswithouthours


#@app.before_request
#def before_request():
    #if not (request.path.startswith('/static') or request.path.endswith('favicon.ico') or request.path.endswith('favicon.ico/')):
        #if request.host == 'm.horsrancher.com': return render_template('mobile-placeholder.html')
        #elif request.host != 'horsrancher.com': return '403 Forbidden', 403

@app.after_request
def after_request(response):
    if request.path.startswith('/static') or request.path.endswith('favicon.ico') or request.path.endswith('favicon.ico/'):
        return response
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route('/<path:url>/favicon.ico')
def favicon_send(url):
    return send_file('static/assets/brand/favicon.ico')

@app.route('/favicon.ico')
def favicon_simple():
    return send_file('static/assets/brand/favicon.ico')

@app.route('/')
def temp_redir():
    return helpers.template_gen("app/index.html")

@app.route('/center/<int:centreID>/')
def centerDisplay(centreID):
    center_info = helpers.database.execute_without_freezing('SELECT * FROM center WHERE id = ?', centreID)
    if len(center_info) == 0:
        return helpers.template_gen('app/error.html', err_code=404), 404
    center_info = center_info[0]
    
    horses_info = helpers.database.execute_without_freezing('SELECT * FROM horse INNER JOIN level ON horse.levelid = level.ID WHERE horse.centerID = ?;', centreID)
    
    instructors_info = helpers.database.execute_without_freezing("SELECT * FROM instructor INNER JOIN level ON instructor.levelid = level.ID WHERE instructor.centerID = ?;", centreID)
    
    levels_info = helpers.database.execute_without_freezing("SELECT * FROM level WHERE centerID = ?;", centreID)
    
    social_info = helpers.social.getSocial(centreID)
    
    cal_table, cal_meta = helpers.calendar.buildcalendartable()
    
    return helpers.template_gen('app/center.html', center_name=center_info['displayName'], center_id=centreID, center_logo=center_info['logoLoc'],
    main_photo=center_info['bannerLoc'], center_description_short=center_info['short_description'],
    center_description_long=center_info['long_description'], center_registration=center_info['date_created'],
    center_instructors=instructors_info, center_horses=horses_info, center_levels=levels_info, center_social=social_info, calendar=cal_table, today=cal_meta)

@app.route('/reserve/<int:centreID>/')
def centerReserve(centreID):
    center_info = helpers.database.execute_without_freezing('SELECT * FROM center WHERE id = ?', centreID)

    center_info = center_info[0]
    
    class_length = int(helpers.database.execute_without_freezing('SELECT classes_length FROM center_offering WHERE center_id = ?', centreID)[0]['classes_length'])
    
    cal_meta = helpers.calendar.getmeta()
    
    return helpers.template_gen('app/reserve.html', center_name=center_info['displayName'], center_id=centreID, center_logo=center_info['logoLoc'],
    main_photo=center_info['bannerLoc'], today=cal_meta, time=class_length)

@app.route('/getDayAvailabilityInfo')
def getDayAvailabilityInfo():
    sleep(1.2)
    infor = helpers.database.execute_without_freezing('SELECT * FROM center_offering WHERE center_id = ?', request.args.get('center'))
    if len(infor) < 1:
        return 'Error 404', 404
    elif len(infor) > 1:
        return 'Error 501: WIP', 501
    else:
        infor = infor[0]
        start_class = infor['center_starts_classes']
        end_class=infor['center_ends_classes']
        classes_every=infor['classes_every']
        size_per_level = infor['class_size']
        toSendInfo = []
        levels = helpers.database.execute_without_freezing('SELECT * FROM level WHERE centerID = ?', request.args.get('center'))
        for i in range(start_class, end_class+1, classes_every):
            with_available = 0
            for level in levels:
                ress = helpers.database.execute_without_freezing('SELECT * FROM reservation WHERE level_id = ? AND start_time = ? AND day = ? AND month = ? AND year = ?', level['ID'], i, request.args.get('d'), request.args.get('m'), request.args.get('y'))
                if not len(ress) >= size_per_level: with_available += 1
            if with_available >= len(levels): final_decision = 1
            elif with_available == 0: final_decision = 0
            else: final_decision = 0.5
            toSendInfo.append({
                't':i,
                'a':final_decision
            })
        return json.dumps(toSendInfo)

def getDayTimeAvailabilityInfo(day, month, year, hour, mins, center):
    time = hour*60 + mins
    infor = helpers.database.execute_without_freezing('SELECT * FROM center_offering WHERE center_id = ?', center)
    if len(infor) < 1:
        return 'Error 404', 404
    elif len(infor) > 1:
        return 'Error 501: WIP', 501
    else:
        response=[]
        levels = helpers.database.execute_without_freezing('SELECT * FROM level WHERE centerID = ?', center)
        infor = infor[0]
        for level in levels:
            ress = helpers.database.execute_without_freezing('SELECT * FROM reservation WHERE level_id = ? AND start_time = ? AND day = ? AND month = ? AND year = ?', level['ID'], time, day, month, year)
            instruct = helpers.database.execute_without_freezing('SELECT * FROM instructor WHERE levelID = ?', level['ID'])
            response.append({
                'level':level['ID'],
                'levelName':level['levelName'],
                'cost':level['EUR_hour'],
                'available':(infor['class_size'] * len(instruct))-len(ress)
            })
        return response
    
@app.route('/getGeneratedTemplateResStep2', methods=['POST'])
def templatingResStep2():
    request.json['center'] = int(request.json['center'])
    
    class_length = int(helpers.database.execute_without_freezing('SELECT classes_length FROM center_offering WHERE center_id = ?', request.json['center'])[0]['classes_length'])
    
    availability_info = getDayTimeAvailabilityInfo(request.json['d'], request.json['m'], request.json['y'], request.json['hour'], request.json['mins'], request.json['center'])
    
    return render_template('/reserve/2.html', av_info=availability_info, time=class_length)

@app.route('/getGeneratedTemplateResStep3', methods=['POST'])
def templatingResStep3():
    request.json['center'] = int(request.json['center'])
    request.json['level'] = int(request.json['level'])
    time_needed = (int(request.json['hour'])*60)+int(request.json['mins'])
    size_per_instructor = helpers.database.execute_without_freezing('SELECT class_size FROM center_offering WHERE center_id = ?', request.json['center'])[0]['class_size']
    instructors_for_level = helpers.database.execute_without_freezing('SELECT * FROM instructor WHERE levelID = ?', request.json['level'])
    instructors = []
    for instructor_in_level in instructors_for_level:
        instructors.append({
            'id':int(instructor_in_level['ID']),
            'name':instructor_in_level['Name'],
            'photo':instructor_in_level['pictureURL'],
            'available':(size_per_instructor - int(helpers.database.execute_without_freezing('SELECT COUNT(*) FROM reservation WHERE instructor_id = ? AND start_time = ?', instructor_in_level['ID'], time_needed)[0]['COUNT(*)']))
        })
    horses_for_level = helpers.database.execute_without_freezing('SELECT * FROM horse WHERE levelID = ?', request.json['level'])
    horses=[]
    for horse_in_level in horses_for_level:
        horses.append({
            'id':horse_in_level['ID'],
            'name': horse_in_level['Name'],
            'photo':horse_in_level['pictureURL'],
            'available':(1 - int(helpers.database.execute_without_freezing('SELECT COUNT(*) FROM reservation WHERE horse_id = ? AND start_time = ?', horse_in_level['ID'], time_needed)[0]['COUNT(*)']))
        })
    return render_template('/reserve/3.html', instructors=instructors, horses=horses, center_id=request.json['center'])

@app.route('/getDayTimeAvailabilityInfo')
def getHTTPDayTimeAvailabilityInfo():
    return json.dumps(getDayTimeAvailabilityInfo(request.args.get('d'), request.args.get('m'), request.args.get('y'), int(request.args.get('hour')),int(request.args.get('min')),request.args.get('center')))


@app.route('/reserve/confirm/<int:centreID>/')
def confirmPage(centreID):
    if int(request.args.get('d', 'GH')) < 1 or int(request.args.get('d')) > 31 or int(request.args.get('m', 'GH')) < 1 or int(request.args.get('m')) > 12 or int(request.args.get('hour', 'GH')) > 24 or int(request.args.get('hour')) < 1:
        return helpers.template_gen('app/error.html', err_code=400), 400
    
    center_info = helpers.database.execute_without_freezing('SELECT * FROM center WHERE id = ?', centreID)

    center_info = center_info[0]
    
    class_length = int(helpers.database.execute_without_freezing('SELECT classes_length FROM center_offering WHERE center_id = ?', centreID)[0]['classes_length'])
    
    meta_booking = []
    meta_booking.append({
        'top':'Fecha seleccionada',
        'big':request.args.get('d') +'/'+ request.args.get('m') +'/'+request.args.get('y'),
        'image':'/static/assets/etc/calendar.png/'
    })
    meta_booking.append({
        'top':'Hora seleccionada',
        'big':request.args.get('hour') +':'+ request.args.get('mins'),
        'image':'/static/assets/etc/clock.png/'
    })
    meta_booking.append({
        'top':'Nivel seleccionado',
        'big':helpers.database.execute_without_freezing('SELECT levelName FROM level WHERE ID = ?', request.args.get('level'))[0]['levelName'],
        'image':'/static/assets/etc/level.png/'
    })
    meta_booking.append({
        'top':'Instructor seleccionado',
        'big':helpers.database.execute_without_freezing('SELECT Name FROM instructor WHERE ID = ?', request.args.get('instructor'))[0]['Name'],
        'image':'/static/center-assets/'+str(centreID)+'/instructors/'+helpers.database.execute_without_freezing('SELECT pictureURL FROM instructor WHERE ID = ?', request.args.get('instructor'))[0]['pictureURL'],
        'circle':True
    })
    meta_booking.append({
        'top':'Caballo seleccionado',
        'big':helpers.database.execute_without_freezing('SELECT Name FROM horse WHERE ID = ?', request.args.get('horse'))[0]['Name'],
        'image':'/static/center-assets/'+str(centreID)+'/horses/'+helpers.database.execute_without_freezing('SELECT pictureURL FROM horse WHERE ID = ?', request.args.get('horse'))[0]['pictureURL'],
        'circle':True
    })
    
    cost_eur=helpers.database.execute_without_freezing("SELECT EUR_hour FROM level WHERE ID = ?", request.args.get('level'))[0]['EUR_hour']
    
    return helpers.template_gen('app/confirm.html', center_name=center_info['displayName'], center_id=centreID, center_logo=center_info['logoLoc'], center_description_short=center_info['short_description'],
    main_photo=center_info['bannerLoc'], center_description_long=center_info['long_description'], time=class_length, meta_booking=meta_booking, request_args=request.args, cost_eur=cost_eur)

@app.route('/signin/', methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        return helpers.template_gen('app/signin.html', next=request.args.get('next', '/'))
    else:
        return redirect(request.form.get('next'))


@app.route('/cal_gen')
def calGen():
    cal_table, cal_meta, today_meta = helpers.calendar.buildextendedcalendartable(request.args.get('year'), request.args.get('month'), 1)
    return render_template('reserve/cal.html', calendar=cal_table, cal_meta=cal_meta, today=today_meta)

@app.route('/process-reservation/', methods=['POST'])
def processReservationHTML():
    if request.form.get('name', 'Unspec') == 'Unspec' and request.form.get('name', 'None') == 'None':
        return 'Incomplete name', 400
    contact_info, good_contact = helpers.social.customercontactinfo(request.form.get('phone', 'N'), request.form.get('name', None), request.form.get('email', None))
    if good_contact == False:
        return contact_info
    outcome, done = helpers.reservation_processing.process_reservation(request.form.get('center', 0), request.form.get('level', 0), request.form.get('instructor', 0), request.form.get('horse', 0),
    request.form.get('d', 0), request.form.get('m', 0), request.form.get('y', 0), request.form.get('hour', 0), request.form.get('mins', 0), contact_info)
    if done:
        return 'Hooray'
    else:
        return outcome, 400

@app.route('/manage/')
def manage_home():
    if session.get('center_id_auth') == None:
        session['center_id_auth'] = 1
        to = request.args.get('to')
        to = request.args.get('to').replace(' ','+')
        return redirect(to.replace('%20','+')) #helpers.template_gen('manage.html')
    else:
        return helpers.template_gen('manage/home.html')

@app.route('/manage/instructors/')
def manage_instructors():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    instructors = helpers.database.execute_without_freezing('SELECT instructor.*, level.levelName FROM instructor INNER JOIN level ON instructor.levelID = level.ID WHERE instructor.centerID = ?', session['center_id_auth'])
    return helpers.template_gen('manage/instructors.html', instructors=instructors, center_id=1)
@app.route('/manage/instructors/<int:instructor_id>/edit/', methods=['GET','POST'])
def manage_edit_instructor(instructor_id):
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        #TODO: Check if instructor is part of authorised center
        instructor = helpers.database.execute_without_freezing("SELECT * FROM instructor WHERE id = ?", instructor_id)
        if len(instructor) < 1:
            return helpers.template_gen('manage/error.html', err_code=404), 404
        available_pics = os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/instructors/')
        if instructor[0]['pictureURL'] in available_pics:
            available_pics.remove(instructor[0]['pictureURL'])
        available_level = helpers.database.execute_without_freezing("SELECT * FROM level WHERE centerID = ?", session['center_id_auth'])
        return helpers.template_gen('manage/instructor-edit.html', instructor=instructor[0], center_id=session['center_id_auth'], images=available_pics, levels = available_level, new=False)
    else:
        process_obj = helpers.reservation_processing.update_instructor(instructor_id, request.form.get('name' ,''), request.form.get('pictureURL' ,''), request.form.get('levelID' ,''))
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/instructors/')
@app.route('/manage/instructors/<int:instructor_id>/delete/', methods=['GET','POST'])
def manage_delete_instructor(instructor_id):
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        instructor = helpers.database.execute_without_freezing("SELECT * FROM instructor WHERE id = ?", instructor_id)
        if len(instructor) < 1:
            return helpers.template_gen('manage/error.html', err_code=404), 404
        return helpers.template_gen('manage/instructor-delete.html', instructor=instructor[0], center_id=session['center_id_auth'])
    else:
        process_obj = helpers.reservation_processing.delete_instructor(instructor_id)
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/instructors/')
@app.route('/manage/instructors/+/edit', methods=['GET','POST'])
def manage_new_instructor():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        available_pics = os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/instructors/')
        available_level = helpers.database.execute_without_freezing("SELECT * FROM level WHERE centerID = ?", session['center_id_auth'])
        return helpers.template_gen('manage/instructor-edit.html', instructor={'Name':'','pictureURL':'../../../assets/etc/missing-profile.png',}, center_id=session['center_id_auth'], images=available_pics, levels=available_level, new=True)
    else:
        process_obj = helpers.reservation_processing.update_instructor('+', request.form.get('name' ,''), request.form.get('pictureURL' ,''), request.form.get('levelID' ,''))
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/instructors/')

@app.route('/manage/horses/')
def manage_horses():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    horses = helpers.database.execute_without_freezing('SELECT horse.*, level.levelName FROM horse INNER JOIN level ON horse.levelID = level.ID WHERE horse.centerID = ?', session['center_id_auth'])
    return helpers.template_gen('manage/horses.html', horses=horses, center_id=1)
@app.route('/manage/horses/<int:horse_id>/edit/', methods=['GET','POST'])
def manage_edit_horse(horse_id):
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        #TODO: Check if horse is part of authorised center
        horse = helpers.database.execute_without_freezing("SELECT * FROM horse WHERE id = ?", horse_id)
        if len(horse) < 1:
            return helpers.template_gen('manage/error.html', err_code=404), 404
        available_pics = os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/horses/')
        if horse[0]['pictureURL'] in available_pics:
            available_pics.remove(horse[0]['pictureURL'])
        available_level = helpers.database.execute_without_freezing("SELECT * FROM level WHERE centerID = ?", session['center_id_auth'])
        return helpers.template_gen('manage/horse-edit.html', horse=horse[0], center_id=session['center_id_auth'], images=available_pics, levels = available_level, new=False)
    else:
        process_obj = helpers.reservation_processing.update_horse(horse_id, request.form.get('name' ,''), request.form.get('pictureURL' ,''), request.form.get('levelID' ,''))
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/horses/')
@app.route('/manage/horses/<int:horse_id>/delete/', methods=['GET','POST'])
def manage_delete_horse(horse_id):
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        horse = helpers.database.execute_without_freezing("SELECT * FROM horse WHERE id = ?", horse_id)
        if len(horse) < 1:
            return helpers.template_gen('manage/error.html', err_code=404), 404
        return helpers.template_gen('manage/horse-delete.html', horse=horse[0], center_id=session['center_id_auth'])
    else:
        process_obj = helpers.reservation_processing.delete_horse(horse_id)
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/horses/')
@app.route('/manage/horses/+/edit', methods=['GET','POST'])
def manage_new_horse():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        available_pics = os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/horses/')
        available_level = helpers.database.execute_without_freezing("SELECT * FROM level WHERE centerID = ?", session['center_id_auth'])
        return helpers.template_gen('manage/horse-edit.html', horse={'Name':'','pictureURL':'../../../assets/etc/missing-profile.png',}, center_id=session['center_id_auth'], images=available_pics, levels=available_level, new=True)
    else:
        process_obj = helpers.reservation_processing.update_horse('+', request.form.get('name' ,''), request.form.get('pictureURL' ,''), request.form.get('levelID' ,''))
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/horses/')

@app.route('/manage/levels/')
def manage_levels():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    levels = helpers.database.execute_without_freezing('SELECT * FROM level WHERE centerID = ?', session['center_id_auth'])
    return helpers.template_gen('manage/levels.html', levels=levels, center_id=1)
@app.route('/manage/levels/<int:level_id>/edit/', methods=['GET','POST'])
def manage_edit_level(level_id):
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        #TODO: Check if level is part of authorised center
        level = helpers.database.execute_without_freezing("SELECT * FROM level WHERE id = ?", level_id)
        if len(level) < 1:
            return helpers.template_gen('manage/error.html', err_code=404), 404
        return helpers.template_gen('manage/level-edit.html', level=level[0], center_id=session['center_id_auth'], new=False)
    else:
        process_obj = helpers.reservation_processing.update_level(level_id, request.form.get('name' ,''), request.form.get('euros' ,''))
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/levels/')
@app.route('/manage/levels/<int:level_id>/delete/', methods=['GET','POST'])
def manage_delete_level(level_id):
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        level = helpers.database.execute_without_freezing("SELECT * FROM level WHERE id = ?", level_id)
        if len(level) < 1:
            return helpers.template_gen('manage/error.html', err_code=404), 404
        return helpers.template_gen('manage/level-delete.html', level=level[0], center_id=session['center_id_auth'])
    else:
        process_obj = helpers.reservation_processing.delete_level(level_id)
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/levels/')
@app.route('/manage/levels/+/edit', methods=['GET','POST'])
def manage_new_level():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        #TODO: Check if level is part of authorised center
        return helpers.template_gen('manage/level-edit.html', level={'levelName':'', 'EUR_hour':0.00}, center_id=session['center_id_auth'], new=False)
    else:
        process_obj = helpers.reservation_processing.update_level('+', request.form.get('name' ,''), request.form.get('euros' ,''))
        if process_obj == False:
            return helpers.template_gen('manage/error.html', err_code=400), 400
        return redirect('/manage/levels/')

@app.route('/manage/images/')
def manage_images():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    images = []
    maa_images = os.listdir('/root/static/center-assets/'+str(session['center_id_auth']))
    for maa_image in maa_images:
        if os.path.isfile('/root/static/center-assets/'+str(session['center_id_auth'])+'/'+maa_image):
            images.append({
                'url':'/static/center-assets/'+str(session['center_id_auth'])+'/'+maa_image,
                'file':maa_image,
                'type':'Principal',
                'typeR':'main'
            })
    instructor_images = os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/instructors')
    for instructor_image in instructor_images:
        images.append({
            'url':'/static/center-assets/'+str(session['center_id_auth'])+'/instructors/'+instructor_image,
            'file':instructor_image,
            'type':'Profesor',
            'typeR':'instructor'
        })
    horse_images = os.listdir('/root/static/center-assets/'+str(session['center_id_auth'])+'/horses')
    for horse_image in horse_images:
        images.append({
            'url':'/static/center-assets/'+str(session['center_id_auth'])+'/horses/'+horse_image,
            'file':horse_image,
            'type':'Caballo',
            'typeR':'horse'
        })
    return helpers.template_gen('manage/images.html', images=images, center_id=1)
@app.route('/manage/images/<Itype>/<image>/delete/', methods=['GET', 'POST'])
def delete_image(Itype, image):
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method=='GET':
        if Itype == 'main': image_url = '/static/center-assets/'+str(session['center_id_auth'])+'/'+image
        elif Itype == 'instructor': image_url = '/static/center-assets/'+str(session['center_id_auth'])+'/instructors/'+image
        elif Itype == 'horse': image_url = '/static/center-assets/'+str(session['center_id_auth'])+'/horses/'+image
        else: return helpers.template_gen('manage/error.hmtl', err_code=404), 404
        return helpers.template_gen('manage/image-delete.html', picture_url=image_url, picture_name=image)
    else:
        if Itype == 'main': image_url = '/root/static/center-assets/'+str(session['center_id_auth'])+'/'+image
        elif Itype == 'instructor': image_url = '/root/static/center-assets/'+str(session['center_id_auth'])+'/instructors/'+image
        elif Itype == 'horse': image_url = '/root/static/center-assets/'+str(session['center_id_auth'])+'/horses/'+image
        if os.path.exists(image_url):
            os.remove(image_url)
            return redirect('/manage/images')
        else:
            return helpers.template_gen('manage/error.html', err_code=404), 404
@app.route('/manage/images/+/', methods=['GET','POST'])
def new_image():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        return helpers.template_gen('manage/image-new.html')
    else:
         # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'No selected file'
        if file and helpers.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if request.form.get('type') == 'main': image_url = '/root/static/center-assets/'+str(session['center_id_auth'])+'/'
            elif request.form.get('type') == 'instructors': image_url = '/root/static/center-assets/'+str(session['center_id_auth'])+'/instructors/'
            elif request.form.get('type') == 'horses': image_url = '/root/static/center-assets/'+str(session['center_id_auth'])+'/horses/'
            else: return helpers.template_gen('manage/error.html', err_code=400),400
            file.save(os.path.join(image_url, filename))
            return redirect('/manage/images')

@app.route('/manage/info/')
def manage_center_info():
    if session.get('center_id_auth') == None:
        return redirect('/manage/?to='+request.path)
    if request.method == 'GET':
        center_info = helpers.database.execute_without_freezing('SELECT * FROM center WHERE id = ?', session.get('center_id_auth'))
        if len(center_info) == 0:
            return helpers.template_gen('app/error.html', err_code=404), 404
        center_info = center_info[0]
        return helpers.template_gen('manage/center-details.html', center_name=center_info['displayName'], center_id=session.get('center_id_auth'), center_logo=center_info['logoLoc'],
        main_photo=center_info['bannerLoc'], center_description_short=center_info['short_description'],
        center_description_long=center_info['long_description'], center_registration=center_info['date_created'])
    else:
        return 'Boo'


@app.route('/phone_api/get_reservations_under_phone_number/', methods=['POST'])
def phoneRApi():
    if not request.json['phone_api_id'] == "SSE^*DdjdQZw33N&g2S5m$MKUG&WkoUEH#rmSCAuL*!xXru#hHKtYBm*jD#!PaB%jxCziwXiRa9C*m4tMzd88egU*XEeuN#8p5@g!4Esb%N5w8Jp%%JqMZ4e3YbXvaS9":
        return '502', 502
    rrsss = helpers.database.execute_without_freezing("SELECT * FROM reservation INNER JOIN center ON center.ID = reservation.center_id WHERE phone = ?", helpers.social.phonenumbercountry(request.json['phone nmb']))
    if len(rrsss) < 1:
        return '404', 404
    return 'en '+rrsss[0]['displayName'] + ' a las ' + str(int(rrsss[0]['start_time'])//60) + ':' + str(int(rrsss[0]['start_time'])%60) + ' el ' + str(rrsss[0]['day']) + ' de ' + helpers.calendar.getmo(rrsss[0]['month']) + ' de ' + str(rrsss[0]['year'])



def errorhandler(e):
    if request.path.startswith('/manage/'):
        return helpers.template_gen('manage/error.html', err_code=e.code), e.code
    else:
        return helpers.template_gen('app/error.html', err_code=e.code), e.code


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
