from django.db import migrations

def split_names(apps, schema_editor):
    Project = apps.get_model('firingtickets', 'Project')

    for project in Project.objects.all():
        name_parts = project.name.split()
        if len(name_parts) >= 1:
            project.first_name = name_parts[0]
        if len(name_parts) >= 2:
            project.last_name = ' '.join(name_parts[1:])
        project.save()

class Migration(migrations.Migration):

    dependencies = [
       ('firingtickets', '0009_auto_20230709_0101'), 
    ]

    operations = [
        migrations.RunPython(split_names),
        migrations.RemoveField('Project', 'name')
    ]
