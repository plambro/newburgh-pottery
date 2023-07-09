from django.shortcuts import render
from django.http import HttpResponse

from .models import Project
from .forms import ProjectForm
from .csv_utils import *
import pottery.settings as settings

from datetime import datetime
import csv
from collections import defaultdict
import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def create(request):
    context = {}
    if request.POST:
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "firingtickets/success.html")

    else:
        form = ProjectForm()

    context['form'] = form
    return render(request, "firingtickets/create.html", context)

def get_monthly_report(request):
    now = datetime.now()
    month, year = get_previous_month(now.month, now.year)
    output_location = settings.OUTPUT_LOCATION
    member_projects = get_projects_in_month(month, year, Project.MEMBER)
    student_projects = get_projects_in_month(month, year, Project.STUDENT)
    member_totals = calculate_project_totals(member_projects)
    student_totals = calculate_project_totals(student_projects)
    # Write member_totals to member_projects.csv
    write_totals_to_csv(member_totals, output_location, f'{month}_{year}_totals_member_projects.csv')
    # Write student_totals to student_projects.csv
    write_totals_to_csv(student_totals, output_location, f'{month}_{year}_totals_student_projects.csv')
    upload_to_google_drive(output_location, f'{month}_{year}_totals_member_projects.csv')
    upload_to_google_drive(output_location, f'{month}_{year}_totals_student_projects.csv')
    delete_file(os.path.join(output_location, f'{month}_{year}_totals_member_projects.csv'))
    delete_file(os.path.join(output_location, f'{month}_{year}_totals_student_projects.csv'))
    return HttpResponse('OK')

def get_detailed_report(request):
    now = datetime.now()
    month, year = get_previous_month(now.month, now.year)
    output_location = settings.OUTPUT_LOCATION
    member_projects = get_projects_in_month(month, year, Project.MEMBER)
    student_projects = get_projects_in_month(month, year, Project.STUDENT)
    # Write member_totals to member_projects.csv
    write_itemized_to_csv(member_projects, output_location, f'{month}_{year}_itemized_member_projects.csv')
    # Write student_totals to student_projects.csv
    write_itemized_to_csv(student_projects, output_location, f'{month}_{year}_itemized_student_projects.csv')
    upload_to_google_drive(output_location, f'{month}_{year}_itemized_member_projects.csv')
    upload_to_google_drive(output_location, f'{month}_{year}_itemized_student_projects.csv')
    delete_file(os.path.join(output_location, f'{month}_{year}_itemized_member_projects.csv'))
    delete_file(os.path.join(output_location, f'{month}_{year}_itemized_student_projects.csv'))
    return HttpResponse('OK')
