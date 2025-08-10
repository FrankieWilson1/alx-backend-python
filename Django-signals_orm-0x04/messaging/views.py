from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


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
