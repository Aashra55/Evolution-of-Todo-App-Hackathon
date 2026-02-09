#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting Minikube deployment for Todo AI Chatbot Phase V..."

# --- Phase 1: Setup Infrastructure ---
echo "Installing Dapr control plane..."
# Assume Dapr CLI is installed and 'dapr init' has been run, or deploy Dapr to Minikube
# kubectl apply -f <path_to_dapr_install_manifest> 
echo "Dapr control plane installation/verification assumed complete."

echo "Deploying Kafka cluster and topics..."
kubectl apply -f k8s/kafka/strimzi-operator.yaml
kubectl apply -f k8s/kafka/kafka-cluster.yaml
kubectl apply -f k8s/kafka/topics.yaml
echo "Kafka cluster and topics deployed."

echo "Deploying Dapr components..."
kubectl apply -f k8s/dapr/pubsub.yaml
kubectl apply -f k8s/dapr/state-postgresql.yaml # Using state-postgresql as defined
echo "Dapr components deployed."

# --- Phase 2: Deploy Microservices ---
echo "Deploying microservices..."
# Basic service deployment manifests would go here.
# This example assumes a simple deployment for each service.
# In a real scenario, these would be more detailed (e.g., using Helm).

# Frontend Service
kubectl apply -f k8s/frontend/deployment.yaml -f k8s/frontend/service.yaml
echo "Frontend service deployed."

# Chat API Service
kubectl apply -f k8s/services/chat-api/deployment.yaml -f k8s/services/chat-api/service.yaml
echo "Chat API service deployed."

# Notification Service
kubectl apply -f k8s/services/notification/deployment.yaml -f k8s/services/notification/service.yaml
echo "Notification service deployed."

# Recurring Task Service
kubectl apply -f k8s/services/recurring-task/deployment.yaml -f k8s/services/recurring-task/service.yaml
echo "Recurring Task service deployed."

# Audit Log Service
kubectl apply -f k8s/services/audit-log/deployment.yaml -f k8s/services/audit-log/service.yaml
echo "Audit Log service deployed."

# Real-time Sync Service
kubectl apply -f k8s/services/real-time-sync/deployment.yaml -f k8s/services/real-time-sync/service.yaml
echo "Real-time Sync service deployed."

# --- Phase 3: Verification ---
echo "Verifying deployment status..."
echo "Checking pod statuses..."
kubectl get pods -n kafka # Check Kafka pods
kubectl get pods -n dapr-system # Check Dapr sidecars and control plane pods
kubectl get pods -A # Check all pods in all namespaces

echo "Verifying service endpoints..."
kubectl get services -n kafka
kubectl get services -A

echo "Basic connectivity checks..."
echo "Check if frontend is accessible (e.g., port-forward frontend service)"
echo "Check if Chat API is accessible (e.g., via Dapr invocation)"

echo "Minikube deployment complete. Please verify accessibility and functionality."

exit 0
