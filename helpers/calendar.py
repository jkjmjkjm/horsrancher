from datetime import datetime, timedelta

MONTHS = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']


def getmeta():
    today = datetime.now()
    weekday = int(today.strftime('%w'))
    if weekday == 0:
        weekday = 7
    meta = {
        'd':int(today.strftime('%d')),
        'm':int(today.strftime('%m')),
        'y':int(today.strftime('%Y')),
        'mt':MONTHS[int(today.strftime('%m'))-1]
    }
    return meta

def getmo(mo_no):
    return MONTHS[mo_no]

def buildcalendartable():
    today = datetime.now()
    weekday = int(today.strftime('%w'))
    if weekday == 0:
        weekday = 7
    meta = {
        'd':int(today.strftime('%d')),
        'm':int(today.strftime('%m')),
        'y':int(today.strftime('%Y')),
        'mt':MONTHS[int(today.strftime('%m'))-1]
    }
    table=[]
    start = today - timedelta(weekday-1)
    for i in range(4):
        row=[]
        for j in range(7):
            use = start + timedelta(i*7+j)
            row.append({
                'd':int(use.strftime('%d')),
                'm':int(use.strftime('%m')),
                'y':int(use.strftime('%Y')),
                't':int(today.strftime('%d')) == int(use.strftime('%d')) and int(today.strftime('%m')) == int(use.strftime('%m')),
                'sm':int(today.strftime('%m')) == int(use.strftime('%m')) and int(today.strftime('%y')) == int(use.strftime('%y'))
            })
        table.append(row)
        if int((start + timedelta(i*7+j+1)).strftime('%m')) > meta['m'] or int((start + timedelta(i*7+j+1)).strftime('%y')) > meta['y']: break
    return table, meta

def buildextendedcalendartable(year, month, day):
    today = datetime.now()
    start_ish = datetime(int(year), int(month), int(day))
    weekday = int(start_ish.strftime('%w'))
    if weekday == 0:
        weekday = 7
    table=[]
    start = start_ish - timedelta(weekday-1)
    meta_today = {
        'd':int(today.strftime('%d')),
        'm':int(today.strftime('%m')),
        'y':int(today.strftime('%Y')),
        'mt':MONTHS[int(today.strftime('%m'))-1]
    }
    meta = {
        'd':int(start_ish.strftime('%d')),
        'm':int(start_ish.strftime('%m')),
        'y':int(start_ish.strftime('%Y')),
        'mt':MONTHS[int(start_ish.strftime('%m'))-1]
    }
    for i in range(6):
        row=[]
        for j in range(7):
            use = start + timedelta(i*7+j)
            row.append({
                'd':int(use.strftime('%d')),
                'm':int(use.strftime('%m')),
                'y':int(use.strftime('%Y')),
                't':int(today.strftime('%d')) == int(use.strftime('%d')) and int(today.strftime('%m')) == int(use.strftime('%m')) and int(start_ish.strftime('%y')) == int(use.strftime('%y')),
                'sm':int(start_ish.strftime('%m')) == int(use.strftime('%m')) and int(start_ish.strftime('%y')) == int(use.strftime('%y'))
            })
        table.append(row)
        if int((start + timedelta(i*7+j+1)).strftime('%m')) > meta['m'] or int((start + timedelta(i*7+j+1)).strftime('%y')) > meta['y']: break
    return table, meta, meta_today
