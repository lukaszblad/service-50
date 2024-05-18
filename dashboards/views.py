from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from tickets.models import User, Incident, State, Service, Configuration_Item, Team

# Create your views here.
@login_required
def default_dashboard(request):
    active_status = State.objects.get(state="In progress")
    resolved_status = State.objects.get(state="Resolved")
    assigned_incidents = Incident.objects.filter(assigned_to=request.user, state=active_status)
    resolved_incidents = Incident.objects.filter(resolved_by=request.user, state=resolved_status)
    return render(request, "dashboards/default_dashboard.html", {
        "assigned_incidents":assigned_incidents,
        "resolved_incidents":resolved_incidents,
    })

@login_required
def profile_dashboard(request, owner_username):
    try:
        profile_owner = User.objects.get(username=owner_username)
    except:
        raise Http404
    user_teams = Team.objects.filter(members=profile_owner)
    user_cis = Configuration_Item.objects.filter(owner=profile_owner)
    return render(request, "dashboards/profile_dashboard.html", {
        "profile_owner": profile_owner,
        "user_teams": user_teams,
        "user_cis": user_cis,
    })

@login_required
def team_dashboard(request, team_code):
    try:
        team = Team.objects.get(code=team_code)
    except:
        raise Http404
    members = team.members.all()
    active_state = State.objects.get(state="In progress")
    active_incidents = Incident.objects.filter(assignment_group=team, state=active_state)
    return render(request, "dashboards/team_dashboard.html", {
        "team": team,
        "members": members,
        "active_incidents": active_incidents
    })

@login_required
def configuration_item_dashboard(request, ci_code):
    try:
        ci = Configuration_Item.objects.get(code=ci_code)
    except:
        raise Http404
    return render(request, "dashboards/ci_dashboard.html", {
        "ci":ci,
    })

@login_required
def service_dashboard(request, service_code):
    try:
        service = Service.objects.get(service=service_code)
    except:
        raise Http404
    support_groups = service.support_groups.all()
    print(support_groups)
    return render(request, "dashboards/service_dashboard.html", {
        "service":service,
        "support_groups":support_groups,
    })
