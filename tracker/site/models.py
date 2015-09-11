from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from djangae.fields import RelatedSetField

from djangae.contrib.consistency.signals import connect_signals
connect_signals()

class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return self.title


class Ticket(TimeStampedModel):
    TICKET_STATUS = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, related_name="tickets")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="created_tickets")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="updated_tickets")
    status = models.CharField(max_length=100, choices=TICKET_STATUS,
                              default='OPEN')
    assignees = RelatedSetField(
        settings.AUTH_USER_MODEL, related_name="tickets")

    def __str__(self):
        return self.title
