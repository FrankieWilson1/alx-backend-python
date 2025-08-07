import os
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
import collections
import json


class RequestLoggingMiddleware:
    """A class for request middleware"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Get the authenticated user or 'AnonymousUser'
        user = request.user
        if user.is_authenticated:
            user_info = f"{user.first_name}\
                {user.last_name} ({user.user_id})"
        else:
            user_info = "AnonymousUser"

        # Log the request details
        log_entry = f"{datetime.now()} - \
            User: {user_info} - Path: {request.path}\n"

        # Specify the path for the log file
        log_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'requests.log'
        )

        with open(log_file_path, 'a') as log_file:
            log_file.write(log_entry)

        return response


class RestrictAccessByTimeMiddleware:
    """
    A middleware class to enforce time-based access control
    The primary logic is to check ther server time and return a 404 Forbidden
    error if the request is made outside the allowed time window
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()

        # Access is only allowed between 6 PM and 9 PM (18:00 to 21:00)
        if (current_time.hour >= 18 and current_time.hour < 21):
            return HttpResponseForbidden(
                "Access to this service is restricted outside of 6PM and 9PM."
            )

        response = self.get_response(request)
        return response


class RateLimitingMiddleware:
    """
    A class that uses simple in-memory cache to tract the number of requests
    from each IP address within a one-minute window
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = collections.defaultdict(list)
        self.limit = 5
        self.time_window = 60   # in seconds.

    def __call__(self, request):
        if 'messages' in request.path and request.method == 'POST':
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
            if not ip_address:
                ip_address = request.META.get('REMOTE_ADDR')

            current_time = datetime.now()

            # Clean up old requests from the history
            self.requests[ip_address] = [
                ts for ts in self.requests[ip_address]
                if current_time - ts < timedelta(seconds=self.time_window)
            ]

            if len(self.requests[ip_address]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded. You can only send\
                        5 messages per minute."
                )

            self.requests[ip_address].append(current_time)

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    A class that inspect the request body of incoming chat messages for a list
    of predefined words
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.OFFENSIVE_WORDS = [
            'badword',
            'swear',
            'spam',
            'rude',
            'insult',
            'crazy',
            'retard',
            'lame'
        ]

    def __call__(self, request):
        if request.path.endswith('/messages/') and request.method == 'POST':
            try:
                # Get the message data by reading the body
                body = json.loads(request.body)
                message_body = body.get('message_body', '').lower()

                # Checks for offensive words
                if any(word in message_body for word in self.OFFENSIVE_WORDS):
                    return HttpResponseForbidden(
                        "Your message contains offensive language\
                            and cannot be sent."
                    )
            except (json.JSONDecodeError, UnicodeError):
                pass

        response = self.get_response(request)
        return response


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        required_roles = ['admin', 'moderator']
        protected_path_prefix = '/api/v1/conversations/'

        if request.path.startswith(protected_path_prefix):
            user = request.user
            
            # Add this line to debug the user object
            print(f"DEBUG: User is '{user}' and is_authenticated is '{user.is_authenticated}'")

            if user.is_authenticated:
                user_roles = [group.name for group in user.groups.all()]
                if not any(role in user_roles for role in required_roles):
                    return HttpResponseForbidden("You do not have the required permissions to access this resource.")
            else:
                return HttpResponseForbidden("You must be logged in to access this resource.")

        response = self.get_response(request)
        return response
