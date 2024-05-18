import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# import models
from .models import User, Incident, State, Priority, Location, Service, Configuration_Item, Team, Note
from codes.views import incident_code

# APIs
@login_required
def get_current_user(request):
    current_user = User.objects.get(username=request.user)
    response = {
        "full_name": current_user.first_name + " " + current_user.last_name,
        "username": current_user.username,
    }
    return JsonResponse(response, safe=False)

@login_required
def index(request):
    return render(request, "tickets/index.html")

@login_required
def incident(request, code):
    try:
        incident = Incident.objects.get(number=code)
    except:
        raise Http404
    try:
        messages_list = list(messages.get_messages(request))[0]
        print(messages_list)
        error_message = messages_list
    except:
        error_message = "None"
    states = State.objects.all()
    priorities = Priority.objects.all()
    notes = Note.objects.filter(parent=incident).order_by("-created_on")
    return render(request, 'tickets/incident.html', {
        "states":states,
        'priorities':priorities,
        "incident":incident,
        "notes": notes,
        "error": error_message,
    })

@login_required
def new_incident(request):
    number = incident_code()
    state = State.objects.get(state="New")
    Incident.objects.create(number=number, state=state)
    return HttpResponseRedirect("/incident/" + str(number))

@login_required
def update_incident(request):
    if request.method == 'POST':
        try:
            incident = Incident.objects.get(number=request.POST['incident-number'])
        except:
            return HttpResponseRedirect(reverse("index"))
        if incident.state != State.objects.get(state="Resolved"):
            caller_name = request.POST['caller'].split()
            try:
                incident.caller = User.objects.get(first_name=caller_name[0], last_name=caller_name[1])
            except:
                messages.error(request, "Invalid caller")
                return HttpResponseRedirect("/incident/" + str(incident.number))
            try:
                incident.location = Location.objects.get(location=request.POST['location'])
            except:
                messages.error(request, "Invalid location")
                return HttpResponseRedirect("/incident/" + str(incident.number))
            try:
                incident.service = Service.objects.get(service=request.POST['service'])
            except:
                messages.error(request, "Invalid service")
                return HttpResponseRedirect("/incident/" + str(incident.number))
            try:
                incident.configuration_item = Configuration_Item.objects.get(code=request.POST['configuration-item'])
            except:
                messages.error(request, "Invalid configuration item")
                return HttpResponseRedirect("/incident/" + str(incident.number))
            try:
                incident.priority = Priority.objects.get(code=request.POST['priority'])
            except:
                messages.error(request, "Invalid priority")
                return HttpResponseRedirect("/incident/" + str(incident.number))
            try:
                incident.assignment_group = Team.objects.get(code=request.POST['assignment-group'])
            except:
                messages.error(request, "Invalid assignment group")
                return HttpResponseRedirect("/incident/" + str(incident.number))
            assignee = request.POST['assignee'].split()
            try:
                incident.assigned_to = User.objects.get(first_name=assignee[0], last_name=assignee[1])
            except:
                messages.error(request, "Invalid assignee")
                return HttpResponseRedirect("/incident/" + str(incident.number))
            incident.short_description = request.POST['short-description']
            incident.description = request.POST['description']
            incident.confidential_notes = request.POST['confidential-notes']
            if request.POST['state'] == "Resolved":
                try:
                    incident.state = State.objects.get(state="Resolved")
                except:
                    messages.error(request, "Invalid state")
                    return HttpResponseRedirect("/incident/" + str(incident.number))
                incident.resolved_on = datetime.datetime.now()
                resolvee_name = request.POST['resolved-by'].split()
                try:
                    incident.resolved_by = User.objects.get(first_name=resolvee_name[0], last_name=resolvee_name[1])
                except:
                    messages.error(request, "Invalid resolvee")
                    return HttpResponseRedirect("/incident/" + str(incident.number))
                incident.resolution_notes = request.POST["resolution-notes"]
            else:
                incident.state = State.objects.get(state="In progress")
            incident.save()
        return HttpResponseRedirect("/incident/" + str(incident.number))
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required   
def incident_information(request, code):
    try:
        incident = Incident.objects.get(number=code)
    except:
        return HttpResponseRedirect(reverse("index"))
    response = {
        "state":str(incident.state),
        "priority": str(incident.priority),
        "assignee": str(incident.assigned_to)
        }
    return JsonResponse(response, safe=False)

@login_required
@csrf_exempt
def work_notes(request, code):
    if request.method == "PUT":
        author = User.objects.get(username=request.user)
        content = request.body.decode('utf-8')
        try:
            incident = Incident.objects.get(number=code)
        except:
            return HttpResponseRedirect(reverse("index"))
        Note.objects.create(author=author, content=content, parent=incident)
        return HttpResponse(status=204)

def login_view(request):
    if request.method == "POST":
        # authenticate user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'tickets/login.html', {
                'error': 'Invalid credentials'
            })
    else:
        return render(request, 'tickets/login.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))