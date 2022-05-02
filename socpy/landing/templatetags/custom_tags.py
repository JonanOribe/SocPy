from django import template
from social.models import Notification

register = template.Library()

@register.inclusion_tag('social/show_notifications.html', takes_context=True)
def show_notifications(context):
    notifications = Notification.objects.filter(to_user=context['request'].user).exclude(user_has_seen=True).order_by('-date')
    return {'notifications':notifications}
