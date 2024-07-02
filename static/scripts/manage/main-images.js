document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("logo").addEventListener("change", () => {
        document.getElementById("logoImg").src = "/static/center-assets/"+ document.getElementById("center_id").innerText + "/" + document.getElementById("logo").value;
    });
    document.getElementById("banner").addEventListener("change", () => {
        document.getElementById("bannerDiv").style.backgroundImage = "url(/static/center-assets/"+ document.getElementById("center_id").innerText + "/" + document.getElementById("banner").value +")";
    });
});
