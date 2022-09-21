from django.forms import ModelForm
from .models import Project
from django.contrib.auth.models import User

class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['potter', 'description', 'length', 'width', 'height', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = User.objects.filter(username=self.request.user.username)