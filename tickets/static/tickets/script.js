document.addEventListener("DOMContentLoaded", () => {
    // Button switch APIs
    function applyStyle(element, style) {
        for (var key in style) {
            if (key === "backgroundColor") {
                element.style.backgroundColor = style[key];
            }
            else if (key === "borderTop") {
                element.style.borderTop = style[key];
            }
        }
    }
    function switchButtonAndSection(oldStyle, newStyle, oldButton, newButton) {
        // change old button style
        applyStyle(oldButton, oldStyle);
        // display none old section
        document.getElementById(oldButton.id.replace("button", "content")).style.display = "none";
        // display block new section
        document.getElementById(newButton.id.replace("button", "content")).style.display = "block";
        // change new button style
        applyStyle(newButton, newStyle)
    }


    // COLLAPSE LATERAL PANEL
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
    // LATERAL PANEL SECTION EXPAND
    const lateralButton = document.querySelectorAll(".lateral-button");
    lateralButton.forEach(function (button) {
        button.onclick = () => {
            const buttonSelector = button.id + "-buttons";
            const section = document.getElementById(buttonSelector);
            if (section.style.display === "block") {
                section.style.display = "none";
            }
            else {
                section.style.display = "block";
            }
        }
    })

    //LATERAL PANEL LAYOUT SELECTION
    // Lateral Panel Styles
    const PanelStandardStyle = {
        "backgroundColor" : "#293e40",
    }

    const PanelSelectedStyle = {
        "backgroundColor" : "#5b8072",
    }
    var selectedLateralSection = "catalog";
    const lateralMainButton = document.querySelectorAll(".lateral-panel-header-button");
    lateralMainButton.forEach(function (lateralButton) {
        lateralButton.onclick = () => {
            const selectedLateralButton = document.getElementById(selectedLateralSection + "-button");
            switchButtonAndSection(PanelStandardStyle, PanelSelectedStyle, selectedLateralButton, lateralButton)
            selectedLateralSection = lateralButton.id.replace("-button", "");
        }
    })

    // LAYOUT SELECTION
    var currentLayout = "notes"

    // Styles
    const standardStyle = {
        "backgroundColor" : "#e6e9eb",
        "borderTop" : "4px solid #cecece",
    }

    const selectedStyle = {
        "backgroundColor" : "white",
        "borderTop" : "4px solid #278efc",
    }

    const selectionButtons = document.querySelectorAll(".selection-button"); 
    selectionButtons.forEach(function (button) {
        button.onclick = () => {
            const selectedButton = document.getElementById(currentLayout + "-button");
            console.log(selectedButton)
            switchButtonAndSection(standardStyle, selectedStyle, selectedButton, button)
            currentLayout = button.id.replace("-button", "");
        }
    });
});