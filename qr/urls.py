from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from qr import views


urlpatterns = [
    path('', views.index, name="index"),

    #QRCODES
    path('create_redirection/', views.create_redirection, name='create_redirection'),
    path('generate/', views.generate_qr_code, name='generate_qr_code'),
    path('myqrcodes/', views.my_qr_codes, name='my_qr_codes'),
    path('delete_qr_code/<int:qr_code_id>/', views.delete_qr_code, name='delete_qr_code'),
    path('redirection/<str:redirecting_link>/', views.redirect_to_original, name='redirect_to_original'),
    path('edit_qr_code/<int:qr_code_id>/', views.edit_qr_code, name='edit_qr_code'),

    #NORMAL LOGIN/REGISTER/LOGOUT
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #DJANGO PASSWORD RESETING (not working)
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #PROFILE/EDIT PROFILE
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]
