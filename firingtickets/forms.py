from django.forms import ModelForm
from .models import Project
from django.utils.translation import gettext_lazy as _

class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['first_name', 'last_name', 'membership', 'description', 'length', 'width', 'height', 'quantity']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'membership': _('Membership Status')
        }
        help_texts = {
            'first_name': _('Your first name.'),
            'last_name': _('Your last name.'),
            'description': _('Optional. A brief project description.'),
            'length': _('Length in inches, minimum 2".'),
            'width': _('Width in inches, minimum 2".'),
            'height': _('Height in inches, minimum 2".')
        }
        error_messages = {
            'first_name': {
                'max_length': _("This writer's name is too long."),
            },
        }