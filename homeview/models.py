from django.db import models


class User(models.Model):
    username = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.username}"


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagePath = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"


class UnknownModel(models.Model):
    imagePath = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
