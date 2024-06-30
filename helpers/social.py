import phonenumbers
import helpers.database as database
from re import fullmatch
from urllib.parse import urlparse


def removetrailingslash(s):
    return s[:-1] if s.endswith('/') else s


def saveSocial(center_id, form_data):
    if removetrailingslash(form_data["wa"]):
        newwa = phonenumbers.format_number(phonenumbers.parse(removetrailingslash(form_data["wa"]), 'ES'), phonenumbers.PhoneNumberFormat.E164)
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'wha'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('wha', ?, ?)", center_id, newwa)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'wha'", center_id)
    
    if removetrailingslash(form_data["telephone"]):
        newphone = phonenumbers.format_number(phonenumbers.parse(removetrailingslash(form_data["phone"]), 'ES'), phonenumbers.PhoneNumberFormat.E164)
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'pho'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('pho', ?, ?)", center_id, newphone)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'pho'", center_id)

    if removetrailingslash(form_data["facebook"]) and fullmatch('^https://(www\.)?facebook.com/([a-zA-Z0-9(\.\?)?]+)/?$', removetrailingslash(form_data["facebook"])):
        facebook_acc = urlparse(removetrailingslash(form_data["facebook"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'fac'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('fac', ?, ?)", center_id, facebook_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'fac'", center_id)

    if removetrailingslash(form_data["instagram"]) and fullmatch('^https://(www\.)?instagram.com/([a-zA-Z0-9_]+)$', removetrailingslash(form_data["instagram"])):
        insta_acc = urlparse(removetrailingslash(form_data["instagram"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'ins'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('ins', ?, ?)", center_id, insta_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'ins'", center_id)

    if removetrailingslash(form_data["linkedin"]) and fullmatch('^https://(www\.)?linkedin.com/in/([a-zA-Z0-9-]+)$', removetrailingslash(form_data["linkedin"])):
        linkedin_acc = urlparse(removetrailingslash(form_data["linkedin"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'lin'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('lin', ?, ?)", center_id, linkedin_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'lin'", center_id)

    if removetrailingslash(form_data["pinterest"]) and fullmatch('^https://(www\.)?pinterest.com/([a-zA-Z0-9_]+)/?$', removetrailingslash(form_data["pinterest"])):
        pinterest_acc = urlparse(removetrailingslash(form_data["pinterest"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'pin'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('pin', ?, ?)", center_id, pinterest_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'pin'", center_id)

    if removetrailingslash(form_data["reddit"]) and fullmatch('^https://(www\.)?reddit.com/user/([a-zA-Z0-9_]+)$', removetrailingslash(form_data["reddit"])):
        reddit_acc = urlparse(removetrailingslash(form_data["reddit"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'red'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('red', ?, ?)", center_id, reddit_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'red'", center_id)

    if removetrailingslash(form_data["tiktok"]) and fullmatch('^https://(www\.)?tiktok.com/@?([a-zA-Z0-9_.]+)$', removetrailingslash(form_data["tiktok"])):
        tiktok_acc = urlparse(removetrailingslash(form_data["tiktok"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'tik'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('tik', ?, ?)", center_id, tiktok_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'tik'", center_id)

    if removetrailingslash(form_data["twitter"]) and fullmatch('^https://(www\.)?twitter.com/([a-zA-Z0-9_]+)$', removetrailingslash(form_data['twitter'])):
        twitter_acc = urlparse(removetrailingslash(form_data["twitter"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'twi'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('twi', ?, ?)", center_id, twitter_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'twi'", center_id)

    if removetrailingslash(form_data["vimeo"]) and fullmatch('^https://(www\.)?vimeo.com/([a-zA-Z0-9]+)$', removetrailingslash(form_data["vimeo"])):
        vimeo_acc = urlparse(removetrailingslash(form_data["vimeo"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'vim'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('vim', ?, ?)", center_id, vimeo_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'vim'", center_id)
    
    if removetrailingslash(form_data["youtube"]) and fullmatch('^https://(www\.)?youtube.com/(user|channel)/([a-zA-Z0-9_-]+)$', removetrailingslash(form_data["youtube"])):
        youtube_acc = urlparse(removetrailingslash(form_data["youtube"])).path.lstrip('/')
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'you'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('you', ?, ?)", center_id, youtube_acc)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'you'", center_id)
    
    if removetrailingslash(form_data["email"]) and fullmatch('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', removetrailingslash(form_data["email"])):
        emailnew = removetrailingslash(form_data["email"])
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'ema'", center_id)
        database.execute_without_freezing("INSERT INTO center_social (type, centerID, account) VALUES ('ema', ?, ?)", center_id, emailnew)
    else:
        database.execute_without_freezing("DELETE FROM center_social WHERE centerID = ? AND type = 'ema'", center_id)


def getSocialToEdit(center_id):
    response = {
        "wa":"",
        "telephone":"",
        "facebook":"",
        "instagram":"",
        "linkedin":"",
        "pinterest":"",
        "reddit":"",
        "tiktok":"",
        "twitter":"",
        "vimeo":"",
        "youtube":"",
        "email":""
    }
    social_accounts = database.execute_without_freezing('SELECT * FROM center_social WHERE centerID = ?;', center_id)
    for social_account in social_accounts:
        if social_account['type'] == 'ins':
            response["instagram"] = 'https://instagram.com/' + social_account['account']+'/'
        
        elif social_account['type'] == 'fac':
            response["facebook"] = 'https://www.facebook.com/'+social_account['account']+'/'

        elif social_account['type'] == 'lin':
            response["linkedin"] = 'https://linkedin.com/'+social_account['account']+'/'

        elif social_account['type'] == 'twi':
            response["twitter"] = 'https://twitter.com/'+social_account['account']+'/'
        
        elif social_account['type'] == 'you':
            response["youtube"] = 'https://youtube.com/'+social_account['account']+'/'

        elif social_account['type'] == 'pin':
            response["pinterest"] = 'https://pinterest.com/'+social_account['account']+'/'
                    
        elif social_account['type'] == 'red':
            response["reddit"] = 'https://reddit.com/u/'+social_account['account']+'/'
              
        elif social_account['type'] == 'vim':
            response["vimeo"] = 'https://vimeo.com/'+social_account['account']+'/'
        
        elif social_account['type'] == 'wha':
            response["wa"] = phonenumbercountry(social_account['account'])

        elif social_account['type'] == 'pho':
            response["telephone"] = phonenumbercountry(social_account['account'])
                    
        elif social_account['type'] == 'tik':
            response["tiktok"] = 'https://tiktok.com/@'+social_account['account']+'/'

        elif social_account['type'] == "ema":
            response["email"] = social_account['account'],
                    
    return response



def getSocial(center_id):
    response=[]
    center_name = database.execute_without_freezing('SELECT displayName FROM center WHERE id = ?;', center_id)[0]['displayName']
    social_accounts = database.execute_without_freezing('SELECT * FROM center_social WHERE centerID = ?;', center_id)
    for social_account in social_accounts:
        if social_account['type'] == 'ins':
            response.append(
                {
                    'logo':'instagram.svg',
                    'url':'https://instagram.com/' + social_account['account']+'/',
                    'display':'@'+social_account['account']
                })
        elif social_account['type'] == 'fac':
            response.append(
                {
                    'logo':'facebook.svg',
                    'url':'https://www.facebook.com/'+social_account['account']+'/',
                    'display':center_name + ' en Facebook'
                })
        elif social_account['type'] == 'lin':
            response.append(
                {
                    'logo':'linkedin.svg',
                    'url':'https://linkedin.com/'+social_account['account']+'/',
                    'display':center_name + ' en Linkedin'
                })
        elif social_account['type'] == 'twi':
            response.append(
                {
                    'logo':'twitter.svg',
                    'url':'https://twitter.com/'+social_account['account']+'/',
                    'display':'@'+social_account['account']
                })
        elif social_account['type'] == 'you':
            response.append(
                {
                    'logo':'youtube.svg',
                    'url':'https://youtube.com/'+social_account['account']+'/',
                    'display':center_name + ' en YouTube'
                })
        elif social_account['type'] == 'pin':
            response.append(
                {
                    'logo':'pinterest.svg',
                    'url':'https://pinterest.com/'+social_account['account']+'/',
                    'display':center_name + ' en Pinterest'
                })
        elif social_account['type'] == 'red':
            response.append(
                {
                    'logo':'reddit.svg',
                    'url':'https://reddit.com/u/'+social_account['account']+'/',
                    'display':center_name + ' en Reddit'
                })
        elif social_account['type'] == 'vim':
            response.append(
                {
                    'logo':'vimeo.svg',
                    'url':'https://vimeo.com/'+social_account['account']+'/',
                    'display':center_name + ' en Vimeo'
                })
        elif social_account['type'] == 'wha':
            response.append(
                {
                    'logo':'whatsapp.svg',
                    'url':'https://wa.me/'+phonenumbercountry(social_account['account'])+'/',
                    'display':phonenumberdisplay(social_account['account'])
                })
        elif social_account['type'] == 'pho':
            response.append(
                {
                    'logo':'phone.svg',
                    'url':'tel:'+phonenumbercountry(social_account['account']),
                    'display':phonenumberdisplay(social_account['account'])
                })
        elif social_account['type'] == 'tik':
            response.append(
                {
                    'logo':'tiktok.svg',
                    'url':'https://tiktok.com/@'+social_account['account']+'/',
                    'display':'@'+social_account['account']
                })
        elif social_account['type'] == "ema":
            response.append(
                {
                    'logo':'email.svg',
                    'url':'mailto:'+social_account['account'],
                    'display':social_account['account']
                })
    return response

def phonenumberdisplay(number):
    return phonenumbers.format_number(phonenumbers.parse(number, None), phonenumbers.PhoneNumberFormat.INTERNATIONAL)

def phonenumbercountry(number):
    return phonenumbers.format_number(phonenumbers.parse(number, None), phonenumbers.PhoneNumberFormat.E164)

def getcenterphone(center_id):
    return database.execute_without_freezing("SELECT * FROM center_social WHERE centerID = ? AND type = 'pho'", center_id)[0]['account']

def getcenterphoneform(center_id):
    return phonenumbers.format_number(phonenumbers.parse(database.execute_without_freezing("SELECT * FROM center_social WHERE centerID = ? AND type = 'pho'", center_id)[0]['account'], None), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    
def customercontactinfo(phone, name, email):
    try:
        return {
            'name':name,
            'email':email,
            'phone':phonenumbers.format_number(phonenumbers.parse(phone, 'ES'), phonenumbers.PhoneNumberFormat.E164),
            'form_phone':phonenumbers.format_number(phonenumbers.parse(phone, 'ES'), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        }, True
    except Exception as e:
        return e, False
    