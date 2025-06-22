from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from users.models import Utilisateur
from .forms import MessageForm
from .models import Conversation, Message


@login_required
def conversation_list(request):
    conversations_qs = Conversation.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    )
    conversations = []
    for conv in conversations_qs:
        conv.other = conv.other_participant(request.user)
        conversations.append(conv)

    return render(
        request,
        "messagerie/conversation_list.html",
        {"conversations": conversations},
    )


@login_required
def conversation_detail(request, user_id):
    other = get_object_or_404(Utilisateur, id=user_id)
    if other == request.user:
        return redirect("conversation_list")

    conversation = Conversation.objects.filter(
        Q(participant1=request.user, participant2=other)
        | Q(participant1=other, participant2=request.user)
    ).first()
    if not conversation:
        conversation = Conversation.objects.create(
            participant1=request.user, participant2=other
        )

    messages = Message.objects.filter(conversation=conversation)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=form.cleaned_data["text"],
            )
            return redirect("conversation_detail", user_id=other.id)
    else:
        form = MessageForm()

    return render(
        request,
        "messagerie/conversation_detail.html",
        {
            "conversation": conversation,
            "messages": messages,
            "form": form,
            "other": other,
        },
    )
