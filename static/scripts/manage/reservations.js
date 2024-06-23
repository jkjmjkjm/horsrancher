function applyFilters() {
    //just hides for now, but later will iterate and check all conditions 
    let DOMarray = document.querySelectorAll('tr')
    DOMarray.forEach((DOMelement) => {
        DOMelement.hidden = true;
    })
}

window.addEventListener("load", (event) => {
    //TODO fix this code pls
    document.getElementById("searchCode").addEventListener(onclick, applyFilters)
    document.getElementById("searchClient").addEventListener(onclick, applyFilters)
    document.getElementById("searchInstructor").addEventListener(onclick, applyFilters)
    document.getElementById("searchLevel").addEventListener(onclick, applyFilters)
    document.getElementById("searchHorse").addEventListener(onclick, applyFilters)
});