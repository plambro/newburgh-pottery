from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create, name="create"),
    path("monthlyreport/", views.get_monthly_report, name="monthly report"),
    path("itemizedreport/", views.get_detailed_report, name="itemized report")
]