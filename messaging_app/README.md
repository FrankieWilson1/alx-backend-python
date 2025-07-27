# Messaging Application API

## Project Overview

This project is a backend API for a real-time messaging application, built with Django REST Framework. It provides endpoints for managing users, conversations, and messages, laying the groundwork for a robust communication platform.

## Features

* **User Management:** API endpoints for creating, listing, retrieving, updating, and deleting user accounts with unique UUIDs.
* **Conversation Management:**
    * Create new conversations with multiple participants.
    * List and retrieve existing conversations.
    * Update and delete conversations.
* **Message Management:**
    * Send messages within existing conversations.
    * List and retrieve messages for specific conversations.
    * Update and delete messages.
* **Django REST Framework:** Leverages DRF for efficient API development, serialization, and viewset handling.
* **SQLite Database:** Simple, file-based database for development.

## Technologies Used

* **Python 3.x**
* **Django 5.x**
* **Django REST Framework 3.x**
* **SQLite3** (default database)
* **UUID** for primary keys

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x**: [Download Python](https://www.python.org/downloads/)
* **pip**: Python's package installer (usually comes with Python)
* **Git**: [Download Git](https://git-scm.com/downloads)

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/FrankieWilson1/alx-backend-python/tree/main/messaging_app
cd alx-backend-python/messaging_app
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Navigate into your project's root directory (where manage.py is)
cd messaging_app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

With your virtual environment activated, install the required Python packages:

```bash
pip install django djangorestframework
# You might want to create a requirements.txt later: pip freeze > requirements.txt
```

### 4. Database Migrations

Apply the database migrations to create the necessary tables for your models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Optional but Recommended)

To access the Django admin panel and manage users/data, create a superuser:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username, email, and password.

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```
The API will now be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

The following API endpoints are available under the `/api/` prefix:

### Users

Endpoints for managing user accounts. Users can be created, listed, retrieved, updated, and deleted.

- **List all users / Create a new user:**
    - **URL:** `/api/users/`
    - **Method:** GET (list), POST (create)

    **POST Request Body Example (JSON):**
    ```json
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone_number": "+1234567890",
        "role": "participant",
        "password": "strong-secure-password-123"
    }
    ```
    (Note: The `password` is required for creation and will be automatically hashed by the API. The `user_id` and `created_at` are read-only and generated automatically.)

    **Permissions:** IsAuthenticated (for GET), AllowAny (for POST, depending on project requirements)

- **Retrieve, Update, or Delete a specific user:**
    - **URL:** `/api/users/{user_id}/` (e.g., `/api/users/a1b2c3d4-e5f6-7890-1234-567890abcdef/`)
    - **Method:** GET (retrieve), PUT/PATCH (update), DELETE (delete)

    **Permissions:** IsAuthenticated (e.g., IsOwnerOrAdmin for update/delete, IsAuthenticated for retrieve)

### Conversations

- **List all conversations / Create a new conversation:**
    - **URL:** `/api/conversations/`
    - **Method:** GET (list), POST (create)

    **POST Request Body Example (JSON):**
    ```json
    {
        "topic": "Daily Standup",
        "participants_id": ["uuid-of-user1", "uuid-of-user2"]
    }
    ```
    (Note: The `participants_id` should be a list of UUID strings of existing users. The authenticated user making the request will be automatically added as a participant if not already included.)

    **Permissions:** IsAuthenticated

- **Retrieve, Update, or Delete a specific conversation:**
    - **URL:** `/api/conversations/{conversation_id}/` (e.g., `/api/conversations/a1b2c3d4-e5f6-7890-1234-567890abcdef/`)
    - **Method:** GET (retrieve), PUT/PATCH (update), DELETE (delete)

    **Permissions:** IsAuthenticated (e.g., IsParticipant or IsOwner)

### Messages

- **List all messages / Send a new message:**
    - **URL:** `/api/messages/`
    - **Method:** GET (list), POST (create)

    **POST Request Body Example (JSON):**
    ```json
    {
        "conversation": "uuid-of-the-conversation",
        "message_body": "Hello, team!"
    }
    ```
    (Note: The sender field is automatically set to the authenticated user.)

    **Permissions:** IsAuthenticated

- **Retrieve, Update, or Delete a specific message:**
    - **URL:** `/api/messages/{message_id}/` (e.g., `/api/messages/a0b0c0d0-e0f0-1000-2000-300040005000/`)
    - **Method:** GET (retrieve), PUT/PATCH (update), DELETE (delete)

    **Permissions:** IsAuthenticated (e.g., IsSender or IsOwner)

## Testing the API

You can test the API using tools like:

- **Browser:** Navigate to `http://127.0.0.1:8000/api/` (after running `python manage.py runserver`) to see the browsable API endpoints.
- **curl:** Command-line tool for making requests.
- **Postman / Insomnia:** Desktop API client tools.
- **Python requests library:** For programmatic testing.
