# Messaging App API

This project is a backend API for a messaging application, built with Django and Django REST Framework. It provides endpoints for user authentication, conversation management, and message sending.

## Features

- **User Authentication:** Secure access to the API using JSON Web Tokens (JWT).
- **Conversations:**
    - Create conversations with a list of participants.
    - Fetch a list of conversations for the authenticated user.
    - Only participants can access a conversation's details.
- **Messages:**
    - Send messages to specific conversations.
    - Fetch all messages within a conversation.
    - Pagination is implemented to limit messages to 20 per page.
    - Filtering is available to retrieve messages by sender or within a specific date range.
- **Permissions:** Custom permissions ensure that only authenticated participants can view conversations and messages.

## Technologies Used

- **Python 3**
- **Django:** Web framework
- **Django REST Framework (DRF):** Toolkit for building REST APIs
- **djangorestframework-simplejwt:** For JWT-based authentication
- **django-filter:** For powerful filtering capabilities
- **PostgreSQL:** As the database backend

## Setup and Installation

Follow these steps to get the project running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/FrankieWilson1/alx-backend-python.git
    cd alx-backend-python/messaging_app
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database setup:**
    - Ensure your PostgreSQL database is running.
    - Create a database for the project and configure your `DATABASES` settings in `messaging_app/settings.py`.

5.  **Run migrations and create a superuser:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

A comprehensive Postman collection is included to test all endpoints.

| Method | URL                                                    | Description                                                                 |
|--------|--------------------------------------------------------|-----------------------------------------------------------------------------|
| `POST` | `/api/v1/token/`                                       | Obtain an access and refresh token with a username and password.            |
| `POST` | `/api/v1/conversations/`                               | Create a new conversation with a list of user IDs.                          |
| `GET`  | `/api/v1/conversations/`                               | List all conversations the authenticated user is a participant of.          |
| `POST` | `/api/v1/conversations/{id}/messages/`                 | Send a new message to a specific conversation.                              |
| `GET`  | `/api/v1/conversations/{id}/messages/`                 | List messages in a specific conversation (paginated by 20).                 |
| `GET`  | `/api/v1/conversations/{id}/messages/?sender={uuid}`   | Filter messages by a specific sender.                                       |
| `GET`  | `/api/v1/conversations/{id}/messages/?sent_at_after...`| Filter messages within a date/time range.                                   |

## Testing

A Postman collection with pre-configured requests is available to test the API.

- **File:** `post_man-Collections.postman_collection.json`
- **Steps:**
    1.  Import the collection into Postman.
    2.  Use the `Get JWT Token` request to authenticate.
    3.  Save the `access` token to an environment variable and use it for all subsequent requests.

## Author

- **Frank Williams Ugwu**