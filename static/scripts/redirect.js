function redirectToIncident(element) {
    url = `../../incident/${element.innerHTML}`;
    window.location.href = url;
}

function redirectToUser(element) {
    url = `../../dashboards/profile_dashboard/${element.innerHTML}`;
    window.location.href = url;
}

function redirectToTeam(element) {
    url = `../../dashboards/team_dashboard/${element.innerHTML}`;
    window.location.href = url;
}

function redirectToCI(element) {
    url = `../../dashboards/configuration_item_dashboard/${element.innerHTML}`;
    window.location.href = url;
}

function redirectToService(element) {
    url = `../../dashboards/service_dashboard/${element.innerHTML}`;
    window.location.href = url;
}

// rows color
const rows = document.querySelectorAll(".ticket-row");
var counter = 0;
rows.forEach((element) => {
    if (counter % 2 === 1) {
        element.style.backgroundColor  = "#f1f3f4";
    }
    counter++;
})