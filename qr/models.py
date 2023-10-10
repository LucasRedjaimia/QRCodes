from django.db import models
from django.contrib.auth.models import User
from django import forms


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pic/')

    def __str__(self):
        return f"{self.user}"


class QRCode(models.Model):
    image = models.ImageField(upload_to='qrcodes/')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    original_link = models.URLField()
    redirect_link = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return f"QR Code for: {self.original_link}"


class QRCodeEditForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['original_link']
