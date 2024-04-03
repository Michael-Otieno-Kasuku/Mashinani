from django.urls import path
from .views import LandingPageView, ApplicationFormView, SuccessPageView,ProgressReportView, LoginView, RegisterView, PasswordResetView, PasswordResetSuccessView, RegisterSuccessPageView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('home/', LandingPageView.as_view(), name='landing_page'),
    path('apply/', ApplicationFormView.as_view(), name='apply'),
    path('success/<str:serial_number>/', SuccessPageView.as_view(), name='success_page'),
    path('progress_report/', ProgressReportView.as_view(), name='progress_report'),
    path('password_reset_success/<str:email_address>/', PasswordResetSuccessView.as_view(), name='password_reset_success'),
    path('register/success/', RegisterSuccessPageView.as_view(), name='register_success'),
]
