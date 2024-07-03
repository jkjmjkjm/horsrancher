import helpers.database
import helpers.accounts
import helpers.mailsender
import helpers.payments
import helpers.social
import helpers.calendar
import helpers.reservation_processing
from flask import request, session, render_template
from flask_session import Session
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif', 'bmp', 'tif', 'tiff'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def template_gen(template_name, *args, **kwargs):
    if template_name.startswith("manage/"):
        return render_template(template_name, *args, **kwargs, signed_in=helpers.accounts.signed_in(), current_email = helpers.accounts.current_email(),
                               full_path=request.path, center_role="admin", center_name="TODO");
    else:
        return render_template(template_name, *args, **kwargs, signed_in=helpers.accounts.signed_in(), current_email = helpers.accounts.current_email(),
                               full_path=request.path);

def minstohhmm(mins):
    hours = mins // 60
    mins = mins % 60
    return "{:02d}".format(hours)+':'+"{:02d}".format(mins)

def converttohours(mins):
    return mins // 60

def converttominswithouthours(mins):
    return mins % 60

def hhmmtomins(hhmmstring):
    return int(hhmmstring.split(':')[0]) * 60 + int(hhmmstring.split(':')[1])