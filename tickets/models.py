from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from datetime import datetime

# Rules

# Create your models here.
class Location(models.Model):
    id = models.BigAutoField(primary_key=True)
    location = models.CharField(max_length=128)
    code = models.CharField(max_length=16)

    def __str__ (self):
        return self.code
    
class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=32)

    def __str__ (self):
        return self.role

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=8, validators=[MinLengthValidator(8)], unique=True)
    added_on = models.DateTimeField(default=datetime.now)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="user_location")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name="user_role")
    pass

class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=64)
    members = models.ManyToManyField(User)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="team_manager")

    def __str__ (self):
        return self.code

class Priority(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=16)

    def __str__ (self):
        return self.code

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.CharField(max_length=64)
    support_groups = models.ManyToManyField(Team)

    def __str__ (self):
        return self.service

class OS(models.Model):
    id = models.BigAutoField(primary_key=True)
    specification = models.CharField(max_length=64)

    def __str__ (self):
        return self.specification
    
class Model(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__ (self):
        return self.name

class Configuration_Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=32)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True)
    operating_system = models.ForeignKey(OS, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(default=datetime.now)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__ (self):
        return self.code

class State(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.CharField(max_length=32)

    def __str__ (self):
        return self.state

class Incident(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.CharField(max_length=9, validators=[MinLengthValidator(9)], unique=True)
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="caller", null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    configuration_item = models.ForeignKey(Configuration_Item, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    opened_on = models.DateTimeField(default=datetime.now)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    assignment_group = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_to")
    short_description = models.TextField(null=True)
    description = models.TextField(null=True)
    confidential_notes = models.TextField(null=True)
    resolved_on = models.DateTimeField(null=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="resolved_by", null=True)
    resolution_notes = models.TextField(null=True)

    def __str__ (self):
        return self.number

class Note(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey(Incident, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=datetime.now)
