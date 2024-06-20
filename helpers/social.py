import phonenumbers
import helpers.database as database

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
                    'url':'https://es-es.facebook.com/'+social_account['account']+'/',
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
    