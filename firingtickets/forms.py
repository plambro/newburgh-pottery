from django.forms import ModelForm
from .models import Project
from django.utils.translation import gettext_lazy as _

class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'membership', 'description', 'length', 'width', 'height', 'quantity']
        labels = {
            'name': _('Name'),
            'membership': _('Membership Status')
        }
        help_texts = {
            'name': _('Your full name.'),
            'description': _('Optional. A brief project description.'),
            'length': _('Length in inches, minimum 2".'),
            'width': _('Width in inches, minimum 2".'),
            'height': _('Height in inches, minimum 2".')
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }