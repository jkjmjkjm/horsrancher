/* global dateselected */
/* global timeselected */
/* global Sday */
/* global Smonth */
/* global Syear */
/* global Shours */
/* global Smins */
/* global selected_level */
/* global selected_instructor */
/* global selected_horse */
/* global curr_url */
/* global cal_month */
/* global cal_year */
/* global pass_step */

function specialised_scroll_to(elem_id) {
}

function httpGetAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                callback(xmlHttp);
            }
            else {
                alert(`Something's gone wrong. Please, check your internet connection and reload to try again. If the problem persists, please report it to HorsRancher

Algo ha ido mal. Por favor, revisa tu conexión a internet y recarga la página para volver a intentarlo. Si el problema persiste, por favor informa a HorsRancher

Error code/Código de error:
HTTP ` + xmlHttp.status);
                document.getElementById('oops').hidden = false;
                document.getElementById('err_code').innerHTML = "Error code/Código de error: HTTP "  + xmlHttp.status;
            }
        }
    };
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send();
}

function showLoadingScreen() {
    document.getElementById('loading-content').hidden = false;
    document.getElementById('loading-content').style.opacity = 1;
    document.getElementById('loading-content').className = 'loading-shown'
}
function hideLoadingScreen() {
    document.getElementById('loading-content').style.opacity = 0;
    document.getElementById('loading-content').className = 'loading-hidden';
    setTimeout(function () {
        document.getElementById('loading-content').hidden = true;
    }, 420);
}

function onLoad() {
    selected_instructor = 'N';
    selected_horse = 'N';
    
    pass_step = 0;
    
    cal_month = parseInt(document.getElementById('start_month').innerHTML);
    cal_year = parseInt(document.getElementById('start_year').innerHTML);
    
    curr_url = new URL(window.location.href);
    
    /* if (curr_url.searchParams.get('navigated') != null && curr_url.searchParams.get('navigated') > 0) {
        Sday = parseInt(curr_url.searchParams.get('d'));
        Smonth = parseInt(curr_url.searchParams.get('m'));
        Syear = parseInt(curr_url.searchParams.get('y'));
        Shours = parseInt(curr_url.searchParams.get('hour'));
        Smins = parseInt(curr_url.searchParams.get('mins'))
        if (curr_url.searchParams.get('navigated') == null || curr_url.searchParams.get('y') == null || curr_url.searchParams.get('m') == null || curr_url.searchParams.get('d') == null || curr_url.searchParams.get('hour') == null || curr_url.searchParams.get('mins') == null) {
            alert(`Something's gone wrong. Please, check your internet connection and reload to try again. If the problem persists, please report it to HorsRancher
    
Algo ha ido mal. Por favor, revisa tu conexión a internet y recarga la página para volver a intentarlo. Si el problema persiste, por favor informa a HorsRancher
    
Error:
E01: URL incomplete or malformed`);
            document.getElementById('oops').hidden = false;
            document.getElementById('err_code').innerHTML = "Error code/Código de error: E01: URL incomplete or malformed";
            return 0;
        }
        showLoadingScreen();
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState == 4) {
                if (xmlHttp.status == 200) {
                    document.getElementById('step2-block').innerHTML = xmlHttp.responseText;
                   NO document.getElementById('bottominfo').innerHTML = 'Selecciona un nivel, profesor y caballo para continuar';
                   NO document.getElementById('continuebutton').innerHTML = 'Continuar a finalizar reserva';
                    document.getElementById('continuebutton').disabled = true;
                    hideLoadingScreen();
                    history.replaceState('2ndscreen', '2 Screen','/reserve/'+document.getElementById('center-id').innerHTML+'/'+Syear+'/'+Smonth+'/'+Sday+'/'+Shours+'/'+("00" + Smins).slice (-2)+'/select-level/');
                }
                else {
                    alert(`Something's gone wrong. Please, check your internet connection and reload to try again. If the problem persists, please report it to HorsRancher
    
Algo ha ido mal. Por favor, revisa tu conexión a internet y recarga la página para volver a intentarlo. Si el problema persiste, por favor informa a HorsRancher
    
Error code/Código de error:
HTTP ` + xmlHttp.status);
                    document.getElementById('oops').hidden = false;
                    document.getElementById('err_code').innerHTML = "Error code/Código de error: HTTP "  + xmlHttp.status;
                }
            }
        };
        xmlHttp.open("POST", '/getGeneratedTemplateResStep2', true); // true for asynchronous 
        xmlHttp.setRequestHeader("Content-Type", "application/json");
        xmlHttp.send(JSON.stringify({
            'd':Sday,
            'm':Smonth,
            'y':Syear,
            'hour':Shours,
            'mins':Smins,
            'center':document.getElementById('center-id').innerHTML
        }));
    }
    else { */
        
        if (curr_url.searchParams.get('y') != null && curr_url.searchParams.get('m') != null && curr_url.searchParams.get('d') != null) {
            pass_step = 1;
            cal_month = curr_url.searchParams.get('m');
            cal_year = curr_url.searchParams.get('y');
            httpGetAsync('/cal_gen?year='+cal_year+'&month='+cal_month, function(theRequest) {
                document.getElementById('cal').innerHTML = theRequest.responseText;
                clickedDate(curr_url.searchParams.get('d'), curr_url.searchParams.get('m'), curr_url.searchParams.get('y'));
            });
            
        }
        else {
            httpGetAsync('/cal_gen?year='+cal_year+'&month='+cal_month, function(theRequest) {
                document.getElementById('cal').innerHTML = theRequest.responseText;
            });
            hideLoadingScreen();
        }
    //}
}

function clickedDate(day, month, year) {
    showLoadingScreen();
    document.querySelectorAll('.date-cell').forEach(clearBackground);
    document.querySelectorAll('.today-cell').forEach(function (currV, index, arr) {currV.style.backgroundColor = '#f0f0f0'});
    if(document.getElementById(day+'-'+month+'-'+year+'-cell') != null) {
        document.getElementById(day+'-'+month+'-'+year+'-cell').style.backgroundColor = '#a8c0ff';
    }
    httpGetAsync('/getDayAvailabilityInfo?d='+day+'&m='+month+'&y='+year+'&center='+document.getElementById('center-id').innerHTML, function(theRequest) {
        document.getElementById('step2-block').innerHTML = 'Selecciona una fecha y una hora para continuar';
        document.getElementById('step3-block').innerHTML = 'Selecciona un nivel para continuar';
        let responded = JSON.parse(theRequest.responseText);
        document.getElementById('time-list').innerHTML = '';
        for (let i = 0; i < responded.length; i++) {
            if(responded[i]['a'] == 1) {
                document.getElementById('time-list').innerHTML += `
                <li class='list-inline-item' style='margin-bottom: 20px;'>
                    <button class='btn btn-outline-success btn-lg' onclick='clickedTime(` + Math.floor(responded[i]['t'] / 60) + `, ` + responded[i]['t'] % 60 + `);' id='` + Math.floor(responded[i]['t'] / 60) + `-` + responded[i]['t'] % 60 + `-button'>` + Math.floor(responded[i]['t'] / 60) + ':' + ("00" + responded[i]['t'] % 60).slice (-2) + `</button>
                </li>
                `;
            }
            else if(responded[i]['a'] == 0) {
                document.getElementById('time-list').innerHTML += `
                <li class='list-inline-item' style='margin-bottom: 20px;'>
                    <button class='btn btn-outline-danger btn-lg' disabled>` + Math.floor(responded[i]['t'] / 60) + ':' + ("00" + responded[i]['t'] % 60).slice (-2) + `</button>
                </li>
                `;
            }
            else {
                document.getElementById('time-list').innerHTML += `
                <li class='list-inline-item' style='margin-bottom: 20px;'>
                    <button class='btn btn-outline-warning btn-lg' onclick='clickedDangerTime(` + Math.floor(responded[i]['t'] / 60) + `, ` + responded[i]['t'] % 60 + `);' id='` + Math.floor(responded[i]['t'] / 60) + `-` + responded[i]['t'] % 60 + `-button'>` + Math.floor(responded[i]['t'] / 60) + ':' + ("00" + responded[i]['t'] % 60).slice (-2) + `</button>
                </li>
                `;
            }
        }
        document.getElementById('datemarker').innerHTML=day+'/'+month+'/'+year;
        dateselected = day+'/'+month+'/'+year;
        Sday = day;
        Smonth = month;
        Syear = year;
        history.replaceState('date','date','/reserve/'+document.getElementById('center-id').innerHTML+'/?y='+Syear+'&m='+Smonth+'&d='+Sday);
        if (curr_url.searchParams.get('hour') != null && curr_url.searchParams.get('mins') != null && pass_step < 2) {
            pass_step = 2;
            document.getElementById(curr_url.searchParams.get('hour')+'-'+parseInt(curr_url.searchParams.get('mins'))+'-button').click();
            curr_url.searchParams.set('hour', null);
            curr_url.searchParams.set('mins', null);
        }
        else {
            hideLoadingScreen();
        }
    });
}

function clearBackground(currentValue, index, arr) {
    currentValue.style.backgroundColor = '#FFFFFF';
}
function clearButton(currentValue, index, arr) {
    currentValue.className = 'btn btn-outline-success btn-lg';
}
function clearDangerButton(currentValue, index, arr) {
    currentValue.className = 'btn btn-outline-warning btn-lg';
}

function clickedTime(hours, mins) {
    timeselected = hours+':'+("00" + mins).slice (-2);
    Shours = hours;
    Smins = mins;
    document.querySelectorAll('.time-button').forEach(clearButton);
    document.querySelectorAll('.time-danger-button').forEach(clearDangerButton);
    document.getElementById(hours+'-'+mins+'-button').className = 'btn btn-dark btn-lg time-button';
    afterTime();
}
function clickedDangerTime(hours, mins) {
    timeselected = hours+':'+("00" + mins).slice (-2);
    Shours = hours;
    Smins = mins;
    document.querySelectorAll('.time-button').forEach(clearButton);
    document.querySelectorAll('.time-danger-button').forEach(clearDangerButton);
    document.getElementById(hours+'-'+mins+'-button').className = 'btn btn-warning btn-lg time-danger-button';
    afterTime();

    
}

function afterTime() {
    history.replaceState('selectedTime','selectedTime', '/reserve/'+document.getElementById('center-id').innerHTML+'/?y='+Syear+'&m='+Smonth+'&d='+Sday+'&hour='+Shours + '&mins=' + ("00" + Smins).slice (-2));
    showLoadingScreen();
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                document.getElementById('step2-block').innerHTML = xmlHttp.responseText;
                document.getElementById('step3-block').innerHTML = 'Selecciona un nivel para continuar'
                if (curr_url.searchParams.get('level') != null && pass_step < 3) {
                    pass_step = 3;
                    clickedLevel(parseInt(curr_url.searchParams.get('level')))
                }
                else {
                    hideLoadingScreen();
                    specialised_scroll_to('step2-header');
                }
            }
            else {
                alert(`Something's gone wrong. Please, check your internet connection and reload to try again. If the problem persists, please report it to HorsRancher

Algo ha ido mal. Por favor, revisa tu conexión a internet y recarga la página para volver a intentarlo. Si el problema persiste, por favor informa a HorsRancher

Error code/Código de error:
HTTP ` + xmlHttp.status);
                document.getElementById('oops').hidden = false;
                document.getElementById('err_code').innerHTML = "Error code/Código de error: HTTP "  + xmlHttp.status;
            }
        }
    };
    xmlHttp.open("POST", '/getGeneratedTemplateResStep2', true); // true for asynchronous 
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify({
        'd':Sday,
        'm':Smonth,
        'y':Syear,
        'hour':Shours,
        'mins':Smins,
        'center':document.getElementById('center-id').innerHTML
    }));
}

function nextCal() {
    showLoadingScreen();
    if (cal_month == 12) {
        cal_month = 1;
        cal_year = parseInt(cal_year) + 1;
    }
    else {
        cal_month = parseInt(cal_month) + 1;
    }
    httpGetAsync('/cal_gen?year='+cal_year+'&month='+cal_month, function(theRequest) {
        document.getElementById('cal').innerHTML = theRequest.responseText;
        hideLoadingScreen();
        if(document.getElementById(Sday+'-'+Smonth+'-'+Syear+'-cell') != null) {
            document.getElementById(Sday+'-'+Smonth+'-'+Syear+'-cell').style.backgroundColor = '#a8c0ff';
        }
    })
}
function backCal() {
    showLoadingScreen();
    if (cal_month == 1) {
        cal_month = 12;
        cal_year = parseInt(cal_year) - 1;
    }
    else {
        cal_month = parseInt(cal_month) - 1;
    }
    httpGetAsync('/cal_gen?year='+cal_year+'&month='+cal_month, function(theRequest) {
        document.getElementById('cal').innerHTML = theRequest.responseText;
        hideLoadingScreen();
        if(document.getElementById(Sday+'-'+Smonth+'-'+Syear+'-cell') != null) {
            document.getElementById(Sday+'-'+Smonth+'-'+Syear+'-cell').style.backgroundColor = '#a8c0ff';
        }
    })
}

function chooseMonth() {
    document.getElementById('month-dropdown').selectedIndex = 0
    document.getElementById('year-dropdown').selectedIndex = 0
    let b_rect = document.getElementById('cal-wrap').getBoundingClientRect();
    document.getElementById('month-selector').style.width = b_rect.width+'px';
    document.getElementById('month-selector').style.height = b_rect.height+'px';
    document.getElementById('month-selector').hidden = false;
    document.getElementById('month-selector').className = 'month-selector month-selector-shown';
}
function stopChooseMonth() {
    document.getElementById('month-selector').className = 'month-selector month-selector-hidden';
    setTimeout(function () {
        document.getElementById('month-selector').hidden = true;
    }, 420);
}

function submitMonthDropdowns() {
    if (document.getElementById('month-dropdown').selectedIndex == 0 || document.getElementById('year-dropdown').selectedIndex == 0) {
        return null;
    }
    cal_month = document.getElementById('month-dropdown').value;
    cal_year = document.getElementById('year-dropdown').value;
    showLoadingScreen()
     httpGetAsync('/cal_gen?year='+cal_year+'&month='+cal_month, function(theRequest) {
        document.getElementById('cal').innerHTML = theRequest.responseText;
        hideLoadingScreen();
        stopChooseMonth();
        if(document.getElementById(Sday+'-'+Smonth+'-'+Syear+'-cell') != null) {
            document.getElementById(Sday+'-'+Smonth+'-'+Syear+'-cell').style.backgroundColor = '#a8c0ff';
        }
    })
}

function clickedLevel(level_id) {
    selected_instructor = 'N';
    selected_horse = 'N';
    document.querySelectorAll('.level-card').forEach(function (curr, count, arr) {curr.style.backgroundColor = '#FFFFFF';});
    document.getElementById('level-'+level_id).style.backgroundColor = 'rgb(168, 192, 255)';
    showLoadingScreen();
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                document.getElementById('step3-block').innerHTML = xmlHttp.responseText;
                history.replaceState('selectedTime','selectedTime', '/reserve/'+document.getElementById('center-id').innerHTML+'/?y='+Syear+'&m='+Smonth+'&d='+Sday+'&hour='+Shours + '&mins=' + ("00" + Smins).slice (-2) + '&level='+ level_id);
                selected_level = level_id;
                hideLoadingScreen();
                specialised_scroll_to('step3-header');
                if (pass_step < 4) {
                    if(curr_url.searchParams.get('instructor') != null && curr_url.searchParams.get('horse') != null) {
                        selected_instructor = parseInt(curr_url.searchParams.get('instructor'));
                        selected_horse = parseInt(curr_url.searchParams.get('horse'));
                        afterInstructorHorse()
                    }
                    else {
                        if(curr_url.searchParams.get('instructor') != null) {
                            selected_instructor = parseInt(curr_url.searchParams.get('instructor'));
                            clickedInstructor(parseInt(curr_url.searchParams.get('instructor')));
                        }
                        if(curr_url.searchParams.get('horse') != null) {
                            selected_horse = parseInt(curr_url.searchParams.get('horse'));
                            clickedHorse(parseInt(curr_url.searchParams.get('horse')));
                        }
                    }
                    pass_step=4;
                }
            }
            else {
                alert(`Something's gone wrong. Please, check your internet connection and reload to try again. If the problem persists, please report it to HorsRancher

Algo ha ido mal. Por favor, revisa tu conexión a internet y recarga la página para volver a intentarlo. Si el problema persiste, por favor informa a HorsRancher

Error code/Código de error:
HTTP ` + xmlHttp.status);
                document.getElementById('oops').hidden = false;
                document.getElementById('err_code').innerHTML = "Error code/Código de error: HTTP "  + xmlHttp.status;
            }
        }
    };
    xmlHttp.open("POST", '/getGeneratedTemplateResStep3', true); // true for asynchronous 
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify({
        'd':Sday,
        'm':Smonth,
        'y':Syear,
        'hour':Shours,
        'mins':Smins,
        'center':document.getElementById('center-id').innerHTML,
        'level':level_id
    }));
}

function clickedInstructor(instructor_id) {
    selected_instructor = instructor_id;
    afterInstructorHorse()
}

function clickedHorse(horse_id) {
    selected_horse = horse_id;
    afterInstructorHorse()
}


function afterInstructorHorse() {
    document.querySelectorAll('.horse-card').forEach(function (curr_value, it, ent_array) {
        if (curr_value.id == 'horse-'+selected_horse) {
            curr_value.style.backgroundColor = 'rgb(168, 192, 255)';
        }
        else {
            curr_value.style.backgroundColor = '#FFFFFF';
        }
    });
    document.querySelectorAll('.instructor-card').forEach(function (curr_value, it, ent_array) {
        if (curr_value.id == 'instructor-'+selected_instructor) {
            curr_value.style.backgroundColor = 'rgb(168, 192, 255)';
        }
        else {
            curr_value.style.backgroundColor = '#FFFFFF';
        }
    });
    history.replaceState('ins_hor_c', 'Instructor Horse Clicked', '/reserve/'+document.getElementById('center-id').innerHTML+'/?y='+Syear+'&m='+Smonth+'&d='+Sday+'&hour='+Shours + '&mins=' + ("00" + Smins).slice (-2) + '&level='+ selected_level+'&instructor='+selected_instructor+'&horse='+selected_horse);
    if (selected_horse != 'N' && selected_instructor != 'N') {
        document.getElementById('finish_button').disabled = false;
    }
    
}

function finish_button() {
    window.location.pathname = '/reserve/confirm/'+document.getElementById('center-id').innerHTML+'/'
}