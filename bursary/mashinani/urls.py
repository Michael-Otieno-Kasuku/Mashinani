from django.urls import path
from .views import LandingPageView, ApplicationFormView, SuccessPageView,ProgressReportView

app_name = "mashinani"

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('apply/', ApplicationFormView.as_view(), name='apply'),
    path('success/<str:serial_number>/', SuccessPageView.as_view(), name='success_page'),
    path('progress_report/', ProgressReportView.as_view(), name='progress_report'),
]
