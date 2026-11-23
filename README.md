# Self-Healing Kubernetes Application

A three-tier application built using **FastAPI, PostgreSQL, Docker, and Kubernetes (Minikube)**. This project demonstrates Kubernetes self-healing, persistent storage, health probes, horizontal pod autoscaling, and load testing.

## Project Overview

The objective of this project is to build and deploy a highly available application that can automatically recover from Pod failures and scale based on CPU utilization.

The application uses FastAPI as the backend, PostgreSQL as the database, and Kubernetes to manage application deployment and infrastructure.

## Architecture

```text
                  Users
                    |
                    v
             Kubernetes Service
                    |
                    v
          FastAPI Application
              (2+ Pods)
                    |
                    v
            PostgreSQL Service
                    |
                    v
             PostgreSQL Pod
                    |
                    v
          Persistent Volume Claim
                    |
                    v
             Persistent Storage


       Locust Load Testing
                |
                v
        Application Service
                |
                v
       Kubernetes HPA Controller
                |
                v
       Automatic Pod Scaling
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Application development |
| FastAPI | REST API development |
| PostgreSQL 16 | Database |
| SQLAlchemy | Database integration |
| Docker | Containerization |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| YAML | Kubernetes resource configuration |
| Metrics Server | CPU and memory metrics for HPA |
| Locust | Load testing |
| Git & GitHub | Version control |

## Project Features

### 1. Three-Tier Application
- FastAPI backend application.
- PostgreSQL relational database.
- Kubernetes Services for internal communication.

### 2. Kubernetes Self-Healing
- Automatically recreates failed application Pods.
- Maintains the desired replica count.
- Uses Deployments and ReplicaSets.

### 3. Persistent Storage
- PostgreSQL data stored using PersistentVolumeClaim.
- Persistent storage survives PostgreSQL Pod recreation.
- Uses Kubernetes StorageClass.

### 4. Health Monitoring
- Liveness Probe checks whether the application is running.
- Readiness Probe checks whether the application can serve requests.
- Startup Probe provides additional startup time.

### 5. Horizontal Pod Autoscaling
- Uses Kubernetes Horizontal Pod Autoscaler.
- Monitors CPU utilization through Metrics Server.
- Minimum replicas: 2.
- Maximum replicas: 10.
- Target CPU utilization: 50%.

### 6. Load Testing
- Uses Locust to generate concurrent HTTP requests.
- Tests multiple API endpoints.
- Uses a CPU-intensive endpoint to demonstrate autoscaling.

### 7. Application Security
- Runs application containers as a non-root user.
- Uses Kubernetes Secrets for database credentials.
- Disables privilege escalation.
- Uses a read-only root filesystem.
- Drops unnecessary Linux capabilities.

## Project Structure

```text
self-healing-k8s/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── requirements.txt
│
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-deployment.yaml
│   └── postgres-service.yaml
│
├── loadtest/
│   ├── locustfile.py
│   └── requirements.txt
│
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Prerequisites

Install the following tools:

- Docker
- kubectl
- Minikube
- Python 3
- Git
- WSL2 Ubuntu (for Windows users)

## Installation and Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/Ramachandra123-jpg/self-healing-kubernetes-app.git

cd self-healing-kubernetes-app
```

### Step 2: Start Minikube

```bash
minikube start --driver=docker
```

Enable Metrics Server:

```bash
minikube addons enable metrics-server
```

Verify the cluster:

```bash
kubectl get nodes
```

### Step 3: Build the Docker Image

```bash
docker build --no-cache -t self-healing-api:v3 .
```

Load the image into Minikube:

```bash
minikube image load self-healing-api:v3
```

### Step 4: Create Kubernetes Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### Step 5: Create PostgreSQL Secret

Generate a database password and create the Kubernetes Secret:

```bash
DB_PASSWORD="$(openssl rand -hex 16)"

kubectl create secret generic postgres-secret \
  --namespace self-healing \
  --from-literal=POSTGRES_USER=appuser \
  --from-literal=POSTGRES_PASSWORD="$DB_PASSWORD" \
  --from-literal=POSTGRES_DB=appdb \
  --from-literal=DATABASE_URL="postgresql+psycopg://appuser:${DB_PASSWORD}@postgres-service:5432/appdb" \
  --dry-run=client -o yaml | kubectl apply -f -

unset DB_PASSWORD
```

**Important:** Keep the password consistent with the initialized PostgreSQL database. Do not regenerate this Secret against an existing database without coordinating a database password change.

### Step 6: Deploy PostgreSQL

Create persistent storage:

```bash
kubectl apply -f k8s/postgres-pvc.yaml
```

Deploy PostgreSQL:

```bash
kubectl apply -f k8s/postgres-deployment.yaml
```

Create PostgreSQL Service:

```bash
kubectl apply -f k8s/postgres-service.yaml
```

### Step 7: Deploy FastAPI Application

```bash
kubectl apply -f k8s/deployment.yaml
```

Create the application Service:

```bash
kubectl apply -f k8s/service.yaml
```

Deploy HPA:

```bash
kubectl apply -f k8s/hpa.yaml
```

### Step 8: Verify Kubernetes Resources

Check Pods:

```bash
kubectl get pods -n self-healing
```

Check Services:

```bash
kubectl get svc -n self-healing
```

Check Deployments:

```bash
kubectl get deployments -n self-healing
```

Check PersistentVolumeClaim:

```bash
kubectl get pvc -n self-healing
```

Check HPA:

```bash
kubectl get hpa -n self-healing
```

## Application Access

Start port forwarding:

```bash
kubectl port-forward svc/self-healing-service 8000:80 -n self-healing
```

Open the following URLs:

| Endpoint | Description |
|---|---|
| `http://127.0.0.1:8000/` | Application home |
| `http://127.0.0.1:8000/docs` | FastAPI Swagger documentation |
| `http://127.0.0.1:8000/info` | Application information |
| `http://127.0.0.1:8000/health/live` | Liveness health check |
| `http://127.0.0.1:8000/health/ready` | Readiness health check |
| `http://127.0.0.1:8000/employees` | Employee records |

## Employee API Testing

Create an employee:

```bash
curl -X POST http://127.0.0.1:8000/employees \
-H "Content-Type: application
