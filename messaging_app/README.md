# Messaging Application API

## Project Overview

This project is a backend API for a real-time messaging application, built with Django REST Framework. It provides endpoints for managing users, conversations, and messages. The application is designed to be deployed to a Kubernetes cluster and leverages a **Blue-Green deployment strategy** for seamless, zero-downtime updates.

## Features

- **User, Conversation, and Message Management**: API endpoints for managing all core resources.
- **Django REST Framework**: Leverages DRF for efficient API development.
- **Docker Integration**: The application and its dependencies are containerized for consistent deployment across environments.
- **Kubernetes Deployment**: All services are managed within a Kubernetes cluster for orchestration and scalability.
- **Blue-Green Deployment**: A robust strategy is implemented to deploy new application versions with zero downtime.

## Technologies Used

- Python 3.x
- Django 5.x
- Django REST Framework 3.x
- **Docker**
- **Kubernetes**
- **Minikube** (for local development)
- **MySQL** (for the database)

## Setup and Deployment to Kubernetes

### Prerequisites

Before you begin, ensure you have the following installed:
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Docker**: Includes Docker Engine and Docker Compose. [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Minikube**: [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
- **kubectl**: [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### 1. Clone the Repository

Clone this repository and navigate into the `messaging_app` directory:

```bash
git clone https://github.com/FrankieWilson1/alx-backend-python
cd alx-backend-python/messaging_app
```

### 2. Start Minikube

Start your local Kubernetes cluster with Minikube. This command sets up the environment and enables the ingress addon.

```bash
minikube start --driver=docker --addons=ingress
eval $(minikube docker-env)
```

### 3. Deploy to Kubernetes

The deployment process is automated using the `kubctl-0x02` script. This script builds your Docker image, creates the necessary Kubernetes resources, and deploys both the "blue" (current) and "green" (new) versions of your application.

First, ensure your secrets are configured. Create a file named `secrets.yaml` and apply it:

```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secrets
type: Opaque
stringData:
  MYSQL_USER: "messaging_app_user"
  MYSQL_PASSWORD: "some_secure_password"
  MYSQL_DATABASE: "messaging_app_db"
```

Then, apply the secrets:

```bash
kubectl apply -f secrets.yaml
```

Next, run the deployment script:

```bash
chmod +x kubctl-0x02
./kubctl-0x02
```

This script will handle the build of the new Docker image and the deployment of all necessary Kubernetes manifests (`blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`).

### 4. Switch Traffic (Blue-Green)

After the script confirms the green deployment is healthy, you can switch all user traffic to the new version by changing the selector in `kubeservice.yaml` and applying the update.

```yaml
# kubeservice.yaml (after update)
...
spec:
  selector:
    app: messaging-app
    version: green # Change from 'blue' to 'green'
...
```

Apply the updated service configuration:

```bash
kubectl apply -f kubeservice.yaml
```

### 5. Access the API

To access the API from your local machine, run the `minikube tunnel` command in a separate terminal window and keep it running.

```bash
minikube tunnel
```

Then, you can access the API at `http://localhost/api/v1/`.

## API Endpoints

The API endpoints remain the same:

- Users: `/api/users/`
- Conversations: `/api/conversations/`
- Messages: `/api/messages/`

## Testing the API

You can test the API using tools like curl or Postman.

```bash
curl http://localhost/api/v1/
