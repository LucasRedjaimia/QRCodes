import hashlib
from datetime import timezone
import random

from django.contrib import messages
from django.core.files import File
import qrcode
from io import BytesIO

from django.utils.text import slugify
from .models import QRCode, QRCodeEditForm, CustomUserCreationForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import UpdateView
from .models import Profile
from django.utils import timezone
from django.shortcuts import redirect
from social_django.utils import psa


def index(request):
    original_link = ""
    return render(request, 'index.html', {'original_link': original_link})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def create_redirection(original_link):
    try:
        redirect_link = generate_unique_redirect(original_link)
        redirecting = QRCode.objects.get(redirect_link=redirect_link)
        redirect_link = create_redirection(original_link)
    except QRCode.DoesNotExist:
        pass
    return redirect_link


def generate_unique_redirect(original_link):
    unique_text = original_link + str(
        random.randint(1, 100000))
    unique_text_hash = hashlib.sha256(unique_text.encode()).hexdigest()

    slug = slugify(unique_text_hash)[:10]

    redirect_link = f"{slug}"

    return redirect_link


@login_required
def generate_qr_code(request):
    if request.method == "POST":
        original_link = request.POST.get('original_link', '')
        redirect_link = create_redirection(original_link)

        sanitized_text = slugify(original_link)
        qr_image = qrcode.make("https://qrcodeslibapp-7078f907bd77.herokuapp.com/redirection/" + redirect_link, box_size=15)
        qr_image_pil = qr_image.get_image()

        stream = BytesIO()
        qr_image_pil.save(stream, format='PNG')
        stream.seek(0)

        user_profile, created = Profile.objects.get_or_create(user=request.user)

        qr_code = QRCode(original_link=original_link, redirect_link=redirect_link, profile=user_profile)
        qr_code.save()
        qr_code.image.save(f'{sanitized_text}.png', File(stream))

        qr_code.created_at = timezone.now()
        qr_code.save()

        qr_codes = QRCode.objects.filter(profile=user_profile)

        return render(request, 'success.html', {'qr_codes': qr_codes, 'qr_code': qr_code, 'qr_text': original_link})


@login_required
def profile_view(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile/profile.html', {'user_profile': user_profile})


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['bio']
    template_name = 'profile/profile_edit.html'
    success_url = '/profile/'


@login_required
def my_qr_codes(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    qr_codes = QRCode.objects.filter(profile=user_profile)

    messages.get_messages(request)

    return render(request, 'myqrcodes/index.html', {'qr_codes': qr_codes})


def delete_qr_code(request, qr_code_id):
    if not request.user.is_authenticated:
        return redirect('login')

    qr_code = get_object_or_404(QRCode, id=qr_code_id)
    if qr_code.profile.user != request.user:
        return redirect('my_qr_codes')

    if request.method == 'POST':
        qr_code.delete()
    return redirect('my_qr_codes')


def edit_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, id=qr_code_id)

    if request.method == 'POST':
        form = QRCodeEditForm(request.POST, instance=qr_code)
        if form.is_valid():
            form.save()
            messages.success(request, 'QR code updated successfully')
            return redirect('my_qr_codes')
    else:
        form = QRCodeEditForm(instance=qr_code)

    return render(request, 'myqrcodes/edit_qr_code.html', {'form': form, 'qr_code': qr_code})


def redirect_to_original(request, redirecting_link):
    # Look up the Redirect object with the given redirecting_link
    redirect_object = get_object_or_404(QRCode, redirect_link=redirecting_link)

    original_link = redirect_object.original_link

    if not original_link.startswith("http://") and not original_link.startswith("https://"):
        original_link = "http://" + original_link

    return redirect(original_link)
