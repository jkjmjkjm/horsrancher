function applyFilters() {
    //just hides for now, but later will iterate and check all conditions 
    let DOMarray = document.querySelectorAll('tbody tr')
    DOMarray.forEach((DOMelement) => {
        var condition = true;
        condition = condition && (DOMelement.getElementsByTagName("td")[0].textContent.toUpperCase().includes(document.getElementById("searchCode").value.toUpperCase()));
        condition = condition && (DOMelement.getElementsByTagName("td")[1].textContent.toUpperCase().includes(document.getElementById("searchClient").value.toUpperCase()));
        condition = condition && (DOMelement.getElementsByTagName("td")[4].textContent.toUpperCase().includes(document.getElementById("searchInstructor").value.toUpperCase()));
        condition = condition && (DOMelement.getElementsByTagName("td")[5].textContent.toUpperCase().includes(document.getElementById("searchLevel").value.toUpperCase()));
        condition = condition && (DOMelement.getElementsByTagName("td")[6].textContent.toUpperCase().includes(document.getElementById("searchHorse").value.toUpperCase()));
        DOMelement.hidden = !condition;
    })
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


function changeDateRangeNormal() {
    //showLoadingScreen();
    if (document.getElementById("selectDate").value == "manual") {
        alert("TODO WIP");
    }
    else {
        showLoadingScreen();
        let OffsetDict = document.getElementById("selectDate");
        httpGetAsync("/manage-raw/reservations-raw/", (response) => {

        });
    }
}

window.addEventListener("load", (event) => {
    document.getElementById("searchCode").addEventListener("keyup", applyFilters);
    document.getElementById("searchClient").addEventListener("keyup", applyFilters);
    document.getElementById("searchInstructor").addEventListener("keyup", applyFilters);
    document.getElementById("searchLevel").addEventListener("keyup", applyFilters);
    document.getElementById("searchHorse").addEventListener("keyup", applyFilters);
    document.getElementById("selectDate").addEventListener("change", changeDateRangeNormal);
    hideLoadingScreen();
});

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