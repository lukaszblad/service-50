from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team, Priority, Service, Location, OS, Model, Configuration_Item, State, Incident, Note, Role

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Priority)
admin.site.register(Service)
admin.site.register(Location)
admin.site.register(OS)
admin.site.register(Model)
admin.site.register(Configuration_Item)
admin.site.register(State)
admin.site.register(Incident)
admin.site.register(Note)
admin.site.register(Role)
