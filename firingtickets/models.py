# django imports
from django.db import models
from django.utils.timezone import now as django_now

# project imports
from firingtickets.utils import print_ticket


class Project(models.Model):
    MEMBER = 'Member'
    STUDENT = 'Student'
    GUEST = 'Guest'
    MEMBERSHIP_CHOICES = [(MEMBER, 'Member'),(STUDENT, 'Student'),(GUEST, 'Guest')]

    first_name = models.CharField(max_length=32, null=False, default='')
    last_name = models.CharField(max_length=32, null=False, default='')
    membership = models.CharField(max_length=32, choices=MEMBERSHIP_CHOICES, default='Member')
    description = models.CharField(max_length=64, null=True)
    length = models.IntegerField(null=False)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
    created = models.DateTimeField()

    def __str__(self):
        return f'Created: {self.created.date()}, Description: {self.description}'

    def total_cost(self):
        cost = str(round(((self.length * self.height * self.width) * 0.05 * self.quantity), 2))
        cents = cost.split('.')[1]
        if len(cents) < 2:
            cost += '0'
        return cost

    def receipt(self):
        return print_ticket(self)

    def save(self, *args, **kwargs):
        if self.length < 2:
            self.length = 2
        if self.width < 2:
            self.width = 2
        if self.height < 2:
            self.height = 2
        if not self.created:
            self.created = django_now()

        # capitalize first and last name on save
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

        super().save(*args, **kwargs)
       #self.receipt()

