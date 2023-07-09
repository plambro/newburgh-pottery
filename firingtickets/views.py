from django.shortcuts import render
from django.http import HttpResponse

from .models import Project
from .forms import ProjectForm
import pottery.settings as settings

from datetime import datetime
import csv
from collections import defaultdict
import subprocess
import os

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
    if now.month == 1:
        month = 12
    else:
        month = now.month - 1
    if now.month == 1:
        year = now.year - 1
    else:
        year = now.year
    output_filename = f'{month}_{year}_totals.csv'
    output_location = settings.OUTPUT_LOCATION
    projects = Project.objects.filter(created__month=month)
    costs = defaultdict(float)
    quantities = defaultdict(int)
    names = []
    costs.setdefault('missing_key', 0.0)
    quantities.setdefault('missing_key', 0)
    for project in projects:
        costs[project.name] += float(project.total_cost())
        quantities[project.name] += project.quantity
        if project.name not in names:
            names.append(project.name)
    headers = ['Name', 'Total Cost', 'Quantity']
    with open(f'{output_location}/{output_filename}', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for name in names:
            cost = str(round(costs[name], 2))
            cents = cost.split('.')[1]
            if len(cents) < 2:
                cost += '0'
            writer.writerow([name, f'${cost}', quantities[name]])
    command = ['rclone', 'copy', f'{output_location}/{output_filename}', 'googledrive:']
    subprocess.run(command)
    os.remove(f'{output_location}/{output_filename}')
    return HttpResponse('OK')

def get_detailed_report(request):
    now = datetime.now()
    if now.month == 1:
        month = 12
    else:
        month = now.month - 1
    if now.month == 1:
        year = now.year - 1
    else:
        year = now.year
    output_filename = f'{month}_{year}_itemized.csv'
    output_location = settings.OUTPUT_LOCATION
    projects = Project.objects.filter(created__month=month).order_by('name')
    headers = ['Name', 'Description', 'Dimensions', 'Quantity', 'Cost', 'Date']
    with open(f'{output_location}/{output_filename}', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for project in projects:
            writer.writerow([project.name, project.description, 
                             f'{str(project.length)} x {str(project.width)} x {str(project.height)}',
                             project.quantity, f'${project.total_cost()}', project.created.date()])
    command = ['rclone', 'copy', f'{output_location}/{output_filename}', 'googledrive:']
    subprocess.run(command)
    os.remove(f'{output_location}/{output_filename}')
    return HttpResponse('OK')
