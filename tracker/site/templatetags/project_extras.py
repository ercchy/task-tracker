"""
Extra template tags for Projects
"""
from django import template

register = template.Library()


@register.filter('get_status_count')
def get_status_count(tickets, status):
    """Returns count of the tickets by status"""

    ref_tickets = [t for t in tickets if t.status == status]

    return len(ref_tickets)
