document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("modifyType").value = "def";
    document.getElementById("modifyType").addEventListener("change", () => {
        window.location.href = document.getElementById("modifyType").value;
    })
});