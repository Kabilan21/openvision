from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from visionapi.adduser import addimage
from .models import User
from visionapi.updatesystem import updateapi
from visionapi.recognition import check
import json
from datetime import datetime, timedelta
from .models import Attendance
from django.template.loader import render_to_string


def homePage(request):
    today = datetime.today()
    queryset = Attendance.objects.filter(timestamp__date=today)
    context = {
        'today': datetime.today(),
        'attendance': queryset
    }
    return render(request, 'homeview/home.html', context=context)


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


def dateAttendace(request):
    date = request.POST.get('date')
    today = datetime.strptime(date, "%Y-%m-%d").date()
    queryset = Attendance.objects.filter(timestamp__date=today)
    print(queryset)
    context = {
        'today': today,
        'attendance': queryset
    }
    html_data = render_to_string(
        'homeview/date_change_template.html', context=context)
    return JsonResponse({'html': html_data})
