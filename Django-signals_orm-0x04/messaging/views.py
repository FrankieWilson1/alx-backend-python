from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from .models import Message


@login_required
def message_detail(request, message_id):
    """
    Retrieves a message and its direct replies in an optimized way
    """
    threaded_messages = Message.objects.get_threaded_messages(
        message_id
    )

    context = {
        'threaded_messages': threaded_messages,
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
