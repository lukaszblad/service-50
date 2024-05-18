from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from tickets.models import User, Incident, Service, Configuration_Item, Team

# Create your views here.
def default_search(request):
    if request.method == "POST":
        try:
            criteria = request.POST["search"]
        except:
            return HttpResponseRedirect(reverse("index"))
        # check if criteria is incident number
        try:
            incident = Incident.objects.get(number=criteria)
            return HttpResponseRedirect("/incident/" + str(incident.number))
        except:
            pass
        # check if criteria is ci code
        try:
            configuration_item = Configuration_Item.objects.get(code=criteria)
            return HttpResponseRedirect("/dashboards/configuration_item_dashboard/" + str(configuration_item.code))
        except:
            pass
        # check if criteria is user username
        try:
            user = User.objects.get(username=criteria)
            return HttpResponseRedirect("/dashboards/profile_dashboard/" + str(user.username))
        except:
            pass
        # check if criteria is team code
        try:
            team = Team.objects.get(code=criteria)
            return HttpResponseRedirect("/dashboards/team_dashboard/" + str(team.code))
        except:
            pass
        # check if criteria is in description o short description of incident
        incident_description = Incident.objects.filter(description__contains=criteria)
        incident_short_description = Incident.objects.filter(short_description__contains=criteria)
        incidents = list(set(incident_short_description.union(incident_description, all=True)))
        # check if criteria matches user
        user_first_name = User.objects.filter(first_name__contains=criteria)
        user_last_name = User.objects.filter(last_name__contains=criteria)
        users = list(set(user_last_name.union(user_first_name, all=True)))
        # check if criteria matches team code
        teams = Team.objects.filter(code__contains=criteria)
        # check if criteria matches service code
        services = Service.objects.filter(service__contains=criteria)
        return render(request, "search/default_search.html", {
            "incidents":incidents,
            "users":users,
            "teams":teams,
            "services":services,
        })
