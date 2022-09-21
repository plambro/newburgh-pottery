from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Project
from .forms import ProjectForm
import pottery.settings as settings

from datetime import datetime
import csv

def index(request):
    projects = Project.objects.order_by('-created')
    template = loader.get_template('firingtickets/index.html')
    context = {'projects': projects}
    return HttpResponse(template.render(context, request))

def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'firingtickets/detail.html', {'project': project})

def create(request):
    context = {}
    if request.POST:
        form = ProjectForm(request, request.POST)

        if form.is_valid():
            form.save()
            return render(request, "firingtickets/success.html")

    else:
        form = ProjectForm(request.user)

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
    monthly_queryset = Project.objects.filter(created__month=month).order_by('potter')
    output_filename = f'{month}_{year}_projects.csv'
    output_location = settings['CSV_OUTPUT_LOCATION']
    headers = ['Name', 'Account Name', 'Total Area', ]

    with open(f'{output_location}/{output_filename}', 'w') as f:
        csv_doc = csv.writer(f)