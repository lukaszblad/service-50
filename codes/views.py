import json
from django.urls import reverse
from django.utils.http import urlencode
from django.core.serializers import serialize
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from tickets.models import User, Team, Service, Location, OS, Model, Configuration_Item, Incident, Role

# Code Creation APIs
def user_code():
    try:
        last_user = User.objects.all().latest('added_on')
        new_code = int(last_user.username[4:]) + 1
    except:
        new_code = 1000
    return  'CS50' + str(new_code)

def ci_code(location):
    ci_location = Location.objects.all().filter(code=location)[0]
    try:
        last_ci = Configuration_Item.objects.filter(location=ci_location).latest('added_on')
        new_code = int(last_ci.code[2:]) + 1
    except:
        new_code = str(location) + '100000'
    return str(location) + str(new_code)

def incident_code():
    try:
        last_incident = Incident.objects.all().latest('opened_on')
        new_code =  int(last_incident.number[3:]) + 1
    except:
        new_code = 100000
    return 'INC' + str(new_code)

# APIs
def search_user(request, criteria, *args):
    criteria = criteria.split()
    for word in criteria:
        username_search = User.objects.filter(username__startswith=word)
        first_name_search = User.objects.filter(first_name__startswith=word)
        last_name_search = User.objects.filter(last_name__startswith=word)
    users = list(set(first_name_search.union(username_search, last_name_search, all=True)))[:5]
    users = json.loads(serialize('json', users))
    for user in users:
        user['fields']['value'] = user['fields']['first_name'] + ' ' + user['fields']['last_name']
    return JsonResponse(users, safe=False)

def search_team(request, criteria):
    criteria = criteria.split()
    for word in criteria:        
        teams_search = Team.objects.filter(code__contains=word)
    teams = list(set(teams_search))[:5]
    teams = json.loads(serialize('json', teams))
    for team in teams:
        team['fields']['value'] = team['fields']['code']
    return JsonResponse(teams, safe=False)

def search_assignees(request, team):
    assignees = Team.objects.get(code=team).members.all()[:5]
    assignees = json.loads(serialize('json', assignees))
    return JsonResponse(assignees, safe=False)

def search_location(request, criteria):
    locations = Location.objects.filter(location__startswith=criteria)[:5]
    locations = json.loads(serialize('json', locations))
    for location in locations:
        location['fields']['value'] = location['fields']['location']
    return JsonResponse(locations, safe=False)

def search_service(request, criteria):
    services = Service.objects.filter(service__startswith=criteria)[:5]
    services = json.loads(serialize('json', services))
    for service in services:
        service['fields']['value'] = service['fields']['service']
    return JsonResponse(services, safe=False)

def search_ci(request, criteria):
    cis = Configuration_Item.objects.filter(code__startswith=criteria)[:5]
    cis = json.loads(serialize('json', cis))
    for ci in cis:
        ci['fields']['value'] = ci['fields']['code']
    return JsonResponse(cis, safe=False)

# Views
def entry_added(request):
    return render(request, 'codes/entry_added.html', {
        'entries': request.GET,
    })

def add_configuration_item(request):
    models = Model.objects.all()
    oss = OS.objects.all()
    locations = Location.objects.all()
    if request.method == "POST":
        try:
            model = Model.objects.get(name=request.POST['model'])
            os = OS.objects.get(specification=request.POST["operating_system"])
            owner_names = request.POST['owner'].split()
            owner = User.objects.get(first_name=owner_names[0], last_name=owner_names[1])
            location = Location.objects.get(code=request.POST['location'])
        except:
            return render(request, 'codes/add_ci.html', {
                "models": models,
                "oss": oss,
                "locations": locations,
                "error": "Incorrect data!"
            })
        code = ci_code(location)
        Configuration_Item.objects.create(code=code, model=model, operating_system=os, owner=owner, location=location)
        entries = {
            'model':model,
            'os':os,
            'owner':owner_names[0] + ' ' + owner_names[1],
            'location':location
        }
        url = reverse('entry_added') + '?' + urlencode(entries)
        return HttpResponseRedirect(url)
    else:
        return render(request, 'codes/add_ci.html', {
            "models": models,
            "oss": oss,
            "locations": locations,
        })
    
def add_user(request):
    locations = Location.objects.all()
    roles = Role.objects.all()
    if request.method == "POST":
        first_name = request.POST['first_name'].strip().upper()
        last_name = request.POST['last_name'].strip().upper()
        username = user_code()
        email = first_name.lower() + '.' + last_name.lower() + '@service50.com'
        try:
            location = Location.objects.get(code=request.POST['location'].upper())
        except:
            return render(request, "codes/add_user.html", {
                'locations':locations,
                "roles": roles,
                "error": "Incorrect location",
            })
        try:
            role = Role.objects.get(role=request.POST['role'])
        except:
            return render(request, "codes/add_user.html", {
                'locations':locations,
                "roles": roles,
                "error": "Incorrect role",
            })
        password = request.POST['password']
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, location=location, role=role)
        user.set_password(password)
        user.save()
        entries = {
            'username':username,
            'first name':first_name,
            'last name':last_name,
            'email address': email,
            'role': role,
        }
        url = reverse('entry_added') + '?' + urlencode(entries)
        return HttpResponseRedirect(url)
    else:
        return render(request, "codes/add_user.html", {
            'locations':locations,
            "roles": roles,
        })
