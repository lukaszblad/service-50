document.addEventListener("DOMContentLoaded", () => {
    const lateralPanel = document.getElementById("lateral-panel");
    const panelArrow = document.getElementById("collapse-panel");
    const panelButtons = document.getElementById("panel-buttons");
    const main = document.querySelector("Main");
    var panelStatus = "widened"
    panelArrow.onclick = () => {
        if (panelStatus === "widened") {
            panelButtons.style.display = "none";
            lateralPanel.style.width = "40px";
            panelArrow.innerHTML = "&#8250";
            main.style.left = "40px";
            panelStatus = "collapsed"
        }
        else {
            lateralPanel.style.width = "250px";
            panelButtons.style.display = "block";
            panelArrow.innerHTML = "&#8249";
            main.style.left = "250px";
            panelStatus = "widened"
        }
    }
})