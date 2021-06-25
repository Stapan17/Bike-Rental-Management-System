from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('pdf/', views.GeneratePDF, name='pdf'),
    path('history/', views.History, name="history"),
    path('home/', views.home, name="home"),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout_user'),
    path('take_bike/', views.take_bike, name='take_bike'),
    path('return_bike/', views.return_bike, name='return_bike'),
    path('contact/', views.contact, name='contact'),
    path('admins/', views.admin, name='admin'),
    path('error/', views.error, name='error'),
    path('payment/', views.payment, name='payment'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('success_take/', views.success_take, name='success_take'),
    path('success_return/', views.success_return, name='success_return'),
]
