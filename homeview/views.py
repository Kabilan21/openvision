from django.shortcuts import render
from django.http import HttpResponse
from visionapi.adduser import addimage
from .models import User
from visionapi.updatesystem import updateapi
from visionapi.recognition import check
import json


def homePage(request):
    return render(request, 'homeview/home.html')


def adduser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user, status = User.objects.get_or_create(username=username)
        addimage(username)
        return HttpResponse("Added successfully...")
    return HttpResponse("Add user to the system..")


def updatesystem(request):
    if request.method == 'POST':
        updateapi()
    return HttpResponse("pass")


def startsystem(request):
    with open("files/controller.json", "w") as outfile:
        json.dump({"status": True}, outfile)
    check()
    return HttpResponse("pass")


def stopsystem(request):
    with open("files/controller.json", "w") as outfile:
        json.dump({"status": False}, outfile)
    return HttpResponse("Stopped successfully...")
