import re
from django import template
import calendar
from datetime import datetime

register = template.Library()

@register.filter
def get_days_in_month(month):
    year = datetime.now().year
    try:
        month = int(month)
        if 1 <= month <= 12:
            return range(1, calendar.monthrange(year, month)[1] + 1)
        else:
            return range(0)  # Retourne une séquence vide pour les mois invalides
    except ValueError:
        return range(0)  # Retourne une séquence vide si la conversion en int échoue

@register.filter(name='split_semicolon')
def split_semicolon(value):
    return re.split(r';\s*', value)

@register.filter(name='split')
def split_filter(value, arg):
    return value.split(arg)

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0