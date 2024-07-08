document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("modifyType").addEventListener("change", () => {
        window.location.href = document.getElementById("modifyType").value;
    })
});