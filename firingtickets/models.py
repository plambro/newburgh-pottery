# django imports
from django.db import models
from django.forms import ModelForm
from django.utils.timezone import now as django_now
import pottery.settings as settings
from django.contrib.auth.models import User

# project imports
from firingtickets.utils import print_ticket


class Project(models.Model):
    potter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    description = models.CharField(max_length=64)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    quantity = models.IntegerField()
    created = models.DateTimeField()

    def __str__(self):
        return f'{self.description}'

    def total_area(self):
        return self.length * self.height * self.width

    def receipt(self):
        return print_ticket(self)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = django_now()
        super().save(*args, **kwargs)
        self.receipt()

