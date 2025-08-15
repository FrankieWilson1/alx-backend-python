# Messaging Application API

## Project Overview
This project is a backend API for a real-time messaging application, built with Django REST Framework. It provides endpoints for managing users, conversations, and messages, laying the groundwork for a robust communication platform. The application is designed to be run in a multi-container environment using Docker Compose, with a MySQL database for data persistence.

## Features

- **User Management**: API endpoints for creating, listing, retrieving, updating, and deleting user accounts with unique UUIDs.
- **Conversation Management**:
  - Create new conversations with multiple participants.
  - List and retrieve existing conversations.
  - Update and delete conversations.
- **Message Management**:
  - Send messages within existing conversations.
  - List and retrieve messages for specific conversations.
  - Update and delete messages.
- **Django REST Framework**: Leverages DRF for efficient API development, serialization, and viewset handling.
- **Docker Integration**: The application and its database are containerized for easy setup and consistent deployment.

## Technologies Used

- Python 3.x
- Django 5.x
- Django REST Framework 3.x
- Docker
- Docker Compose
- MySQL (for the database)
- UUID for primary keys

## Setup Instructions

Follow these steps to get the project up and running on your local machine using Docker Compose.

### Prerequisites
Before you begin, ensure you have the following installed:
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Docker**: Includes Docker Engine and Docker Compose. [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/FrankieWilson1/alx-backend-python/tree/main/messaging_app
cd alx-backend-python/messaging_app
```

### 2. Create the Environment File

Create a new file named `.env` in the `messaging_app` directory. This file will securely store your database credentials. Add the following content to the file, and replace the placeholder passwords with secure values of your own:

```
MYSQL_DATABASE=messaging_app_db
MYSQL_USER=messaging_app_user
MYSQL_PASSWORD="your_secure_password"
MYSQL_ROOT_PASSWORD="your_root_password"
```

### 3. Build and Run the Services

Use Docker Compose to build the application image and start both the web and db services. The `--build` flag is used here to ensure the latest changes are incorporated.

```bash
docker compose up --build -d
```

**Note**: If you encounter a docker-buildx error, run `docker build -t messaging-app .` first, then run `docker compose up -d`.

### 4. Run Database Migrations

Once the services are up, run the Django database migrations to create the necessary tables. This command is executed inside the running web container.

```bash
docker compose exec web python manage.py migrate
```

### 5. Create a Superuser (Optional but Recommended)

To access the Django admin panel, create a superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Access the API

The API will be accessible at `http://127.0.0.1:8000/`. The web service is automatically restarted if you make changes to your Django code.

## API Endpoints

The following API endpoints are available under the `/api/` prefix:

### Users

- **Endpoints for managing user accounts**. Users can be created, listed, retrieved, updated, and deleted.
  
  **List all users / Create a new user**:
  - **URL**: `/api/users/`
  - **Method**: GET (list), POST (create)
  
  **POST Request Body Example (JSON)**:
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
  **Note**: The password is required for creation and will be automatically hashed by the API. The user_id and created_at are read-only and generated automatically.

  **Permissions**: IsAuthenticated (for GET), AllowAny (for POST, depending on project requirements)

- **Retrieve, Update, or Delete a specific user**:
  - **URL**: `/api/users/{user_id}/` (e.g., `/api/users/a1b2c3d4-e5f6-7890-1234-567890abcdef/`)
  - **Method**: GET (retrieve), PUT/PATCH (update), DELETE (delete)
  
  **Permissions**: IsAuthenticated (e.g., IsOwnerOrAdmin for update/delete, IsAuthenticated for retrieve)

### Conversations

- **List all conversations / Create a new conversation**:
  - **URL**: `/api/conversations/`
  - **Method**: GET (list), POST (create)
  
  **POST Request Body Example (JSON)**:
  ```json
  {
    "topic": "Daily Standup",
    "participants_id": ["uuid-of-user1", "uuid-of-user2"]
  }
  ```
  **Note**: The participants_id should be a list of UUID strings of existing users. The authenticated user making the request will be automatically added as a participant if not already included.

  **Permissions**: IsAuthenticated

- **Retrieve, Update, or Delete a specific conversation**:
  - **URL**: `/api/conversations/{conversation_id}/` (e.g., `/api/conversations/a1b2c3d4-e5f6-7890-1234-567890abcdef/`)
  - **Method**: GET (retrieve), PUT/PATCH (update), DELETE (delete)
  
  **Permissions**: IsAuthenticated (e.g., IsParticipant or IsOwner)

### Messages

- **List all messages / Send a new message**:
  - **URL**: `/api/messages/`
  - **Method**: GET (list), POST (create)
  
  **POST Request Body Example (JSON)**:
  ```json
  {
    "conversation": "uuid-of-the-conversation",
    "message_body": "Hello, team!"
  }
  ```
  **Note**: The sender field is automatically set to the authenticated user.

  **Permissions**: IsAuthenticated

- **Retrieve, Update, or Delete a specific message**:
  - **URL**: `/api/messages/{message_id}/` (e.g., `/api/messages/a0b0c0d0-e0f0-1000-2000-300040005000/`)
  - **Method**: GET (retrieve), PUT/PATCH (update), DELETE (delete)
  
  **Permissions**: IsAuthenticated (e.g., IsSender or IsOwner)

## Testing the API

You can test the API using tools like:

- **Browser**: Navigate to `http://127.0.0.1:8000/api/` to see the browsable API endpoints.
- **curl**: Command-line tool for making requests.
- **Postman / Insomnia**: Desktop API client tools.
- **Python requests library**: For programmatic testing.
