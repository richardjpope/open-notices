from django import template

register = template.Library()

@register.filter(name='message_tag_to_callout')
def message_tag_to_callout(value):
    return value.replace('debug', 'secondary').replace('info', 'primary').replace('success', 'success').replace('warning', 'alert').replace('error', 'alert')