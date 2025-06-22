from .models import Message


def unread_message_count(request):
    if request.user.is_authenticated:
        return {
            'unread_messages_count': (
                Message.objects.filter(
                    conversation__participant1=request.user,
                    is_read=False,
                )
                .exclude(sender=request.user)
                .count()
                + Message.objects.filter(
                    conversation__participant2=request.user,
                    is_read=False,
                )
                .exclude(sender=request.user)
                .count()
            )
        }
    return {}
