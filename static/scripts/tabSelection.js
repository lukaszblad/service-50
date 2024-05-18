let selectedElement = 'work-notes';

const tabStyles = {
    "standardStyle" : {
        "backgroundColor" : "#e6e9eb",
        "borderTop" : "4px solid #cecece",
    },
    "selectedStyle" : {
        "backgroundColor" : "white",
        "borderTop" : "4px solid #278efc",
    }
}

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

function switchTab(elementToSelect) {

    // old elements
    oldButton = document.getElementById(selectedElement + "-button");
    oldContent = document.getElementById(selectedElement + "-content");

    // new elements
    elementToSelect = elementToSelect.slice(0, -7);
    newButton = document.getElementById(elementToSelect + "-button");
    newContent = document.getElementById(elementToSelect + "-content");

    // swap
    applyStyle(oldButton, tabStyles['standardStyle']);
    applyStyle(newButton, tabStyles['selectedStyle']);
    oldContent.style.display = "none"
    newContent.style.display = "block";
    selectedElement = elementToSelect
}
