import os
from collections import defaultdict
from .models import Project
import csv
import subprocess
import logging

def get_previous_month(current_month, current_year):
    if current_month == 1:
        return 12, current_year - 1
    else:
        return current_month - 1, current_year

def get_projects_in_month(month, year, membership):
    if membership == Project.MEMBER:
        return Project.objects.filter(created__month=month, created__year=year, membership__in=[Project.MEMBER, Project.GUEST]).order_by('last_name')
    else:
        return Project.objects.filter(created__month=month, created__year=year, membership=membership).order_by('last_name')

def calculate_project_totals(projects):
    totals = defaultdict(lambda: {'cost': 0.0, 'quantity': 0})
    for project in projects:
        cost = float(project.total_cost())
        totals[project.name]['cost'] += cost
        totals[project.name]['quantity'] += project.quantity
    return totals

def write_totals_to_csv(totals, output_location, output_filename):
    headers = ['Name', 'Total Cost', 'Quantity']
    with open(os.path.join(output_location, output_filename), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for name, values in totals.items():
            cost = round(values['cost'], 2)
            formatted_cost = f'${cost:.2f}'
            writer.writerow([name, formatted_cost, values['quantity']])

def write_itemized_to_csv(projects, output_location, output_filename):
    headers = ['Name', 'Description', 'Dimensions', 'Quantity', 'Cost', 'Date']
    with open(f'{output_location}/{output_filename}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for project in projects:
            writer.writerow([
                project.name,
                project.description,
                f'{project.length} x {project.width} x {project.height}',
                project.quantity,
                f'${project.total_cost()}',
                project.created.date()
            ])
    return output_filename

def upload_to_google_drive(output_location, output_filename):
    command = ['rclone', 'copy', os.path.join(output_location, output_filename), 'googledrive:']
    process = subprocess.run(command, capture_output=True, text=True)
    response = process.stdout.strip()
    
    # Logging the response
    logger = logging.getLogger(__name__)
    logger.info(f"Google Drive upload response: {response}")

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)