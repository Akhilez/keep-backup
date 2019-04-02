from django.contrib.auth.models import User
from django.db import models

'''

class Auth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=256)


class Label(models.Model):
    id = ''
    label = ''


class List(models.Model):
    id = ''
    title = ''
    children = []
    labels = []


class ListItem(models.Model):
    text = ''
    checked = ''
    parent = ''


class Note(models.Model):
    id = models.BigIntegerField()
    text = models.TextField()
    title = models.CharField(max_length=256, null=True)
    labels = []

'''
