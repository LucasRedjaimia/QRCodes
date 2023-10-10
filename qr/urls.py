from django.urls import path
from django.contrib.auth import views as auth_views
from qr import views
urlpatterns = [
    path('', views.index, name="index"),
    path('create_redirection/', views.create_redirection, name='create_redirection'),
    path('generate/', views.generate_qr_code, name='generate_qr_code'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('myqrcodes/', views.my_qr_codes, name='my_qr_codes'),
    path('delete_qr_code/<int:qr_code_id>/', views.delete_qr_code, name='delete_qr_code'),
    path('redirection/<str:redirecting_link>/', views.redirect_to_original, name='redirect_to_original'),

]
