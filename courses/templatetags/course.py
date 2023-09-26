from django import template
register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.verbose_name
    except AttributeError:
        return None
