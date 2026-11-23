# Self-Healing Kubernetes Application

## Project Overview
A Python FastAPI application deployed on Kubernetes with automated pod recovery, CPU-based autoscaling, health checks and load testing.

## Technologies
- Python FastAPI
- Docker and Multi-stage Builds
- Kubernetes and Minikube
- Horizontal Pod Autoscaler (HPA)
- Metrics Server
- Locust Load Testing

## Features
- REST API development using FastAPI
- Secure, non-root Docker container
- Kubernetes Deployment and Service
- Liveness and Readiness Probes
- CPU and memory resource requests and limits
- Automatic pod scaling using HPA
- Normal and spike traffic simulation using Locust
- Container crash and pod recovery testing

## Project Architecture
FastAPI → Docker → Kubernetes → Metrics Server → HPA → Locust

## Deployment
1. Build the Docker image.
2. Load the image into Minikube.
3. Deploy Kubernetes manifests.
4. Enable Metrics Server.
5. Configure HPA.
6. Run Locust load tests.
7. Monitor scaling and self-healing.

## Learning Outcomes
Hands-on experience with containerization, Kubernetes orchestration, autoscaling, health probes, load testing and DevOps troubleshooting.
