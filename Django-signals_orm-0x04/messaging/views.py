# messaging/views.py

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    unread_messages = Message.unread.unread_messages.by_user(
        request.user
    )

    context = {
        'unread_messages': unread_messages,
    }

    return render(request, 'inbox.html', context)

@login_required
def send_message(request: HttpRequest) -> HttpResponse:
    """
    A view to handle sending a new message.
    """
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')
        parent_message_id = request.POST.get('parent_message')

        if receiver_id and content:
            receiver_user = get_object_or_404(
                User, user_id=receiver_id
            )
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver_user,
                content=content,
                parent_message_id=parent_message_id if parent_message_id else None
            )
    return redirect('home')

@login_required
def message_detail(request, message_id):
    """
    Retrieves a message and its direct replies in an optimized way
    """
    message = get_object_or_404(
        Message.objects.filter(message_id=message_id).select_related(
            'sender',
            'receiver'
        ).prefetch_related(
            'replies'
        ),
        message_id=message_id
    )

    context = {
        'message': message,
    }

    return render(request, 'message_detail.html', context)

@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    """
    Allows a logged-in user to delete their own account.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()

        return redirect('home')

    return redirect('home')
