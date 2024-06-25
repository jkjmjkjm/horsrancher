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

function changeDateRangeNormal() {
    //TODO call the server.
}

window.addEventListener("load", (event) => {
    //TODO fix this code pls
    document.getElementById("searchCode").addEventListener("keyup", applyFilters)
    document.getElementById("searchClient").addEventListener("keyup", applyFilters)
    document.getElementById("searchInstructor").addEventListener("keyup", applyFilters)
    document.getElementById("searchLevel").addEventListener("keyup", applyFilters)
    document.getElementById("searchHorse").addEventListener("keyup", applyFilters)
});