

function refreshPicture() {
    document.getElementById('pictureDisplay').style.backgroundImage =  "url(/static/center-assets/"+document.getElementById('center_id').innerHTML + "/horses/" + document.getElementById('pictureSelect').value + ")";
}

function checkFirst() {
    if (document.getElementById('levelSelect').value == '') {
        alert('Selecciona nivel para continuar');
        return false;
    }
    if (document.getElementById('nameSelect').value == '') {
        alert('Escribe un nombre para continuar');
        return false;
    }
    return true;
}