# Self-Service Database Anti-Corruption Layer REST API

## Overview

This project implements an anti-corruption layer REST API that maps REST endpoints to SQL queries defined in a configuration YAML file. The system runs on a local Kubernetes cluster using Kind (Kubernetes in Docker) for easy local development and testing.

## Repository Structure

- **src/** – Python application source code.
- **helm/** – Helm charts for the API and PostgreSQL deployments.
- **sql/** – SQL scripts for database creation and population.
- **k8s/** – Kubernetes cluster configuration files (e.g., Kind config).
- **docker-compose.yml** – Docker Compose configuration for local development..

## Local Development Setup

1. **Prerequisites:**
- Install Kind
- Install kubectl

2. **Start the Application:**
   ```bash
   # Launch all services
   docker-compose up -d

   # Check service status
   docker-compose ps
   ```

3. **Test API Endpoints in Local:**
   ```bash
   # Basic endpoint test
   curl http://localhost:3000/myapi

      # Basic endpoint test
   curl http://localhost:3000/myapi2

   # Test with query parameters
   curl "http://localhost:3000/myapi?name=Alice"
   ```

4. **Cleanup:**

   ```bash
   # To stop and remove all containers and networks:
   docker-compose down -v
   ```

5. **Deploy to Kubernetes:**
   ```bash
   # Create local Kubernetes cluster
   kind create cluster --config k8s/kind-config.yaml

   # Navigate to Helm directory
   cd helm

   # Install Helm charts
   helm install registry ./registry
   helm install postgres ./postgres
   helm install anti-corruption-api ./anti-corruption-api
   ```

6. **Test API Endpoints in K8s cluster:**
   ```bash
   # Set up port forwarding
   kubectl port-forward svc/anti-corruption-api 3000:3000

   # In a new terminal, test endpoints
   # Basic endpoint test
   curl http://localhost:3000/myapi

   curl http://localhost:3000/myapi2

   # Test with query parameters
   curl "http://localhost:3000/myapi?name=Alice"
   ```

## GitOps Workflow

### Overview
This project implements a GitOps workflow using GitHub Actions for automated deployments. When changes are pushed to the `helm/` directory in the main branch, it automatically triggers a deployment pipeline that updates the application in the Kubernetes cluster.

### How It Works

1. **Configuration as Code**
   - All infrastructure and application configurations are stored as code in the Git repository
   - Helm charts (`helm/` directory) define the desired state of:
     - Database (PostgreSQL)
     - API service
     - Container registry

2. **Automated Deployment Process**
   - When changes are pushed to `helm/**` in the main branch:
     - GitHub Actions workflow is triggered automatically
     - Helm charts are linted and validated
     - Dependencies are updated
     - Changes are deployed to the Kubernetes cluster

3. **Making Changes**
   To update the application or database configuration:
   1. Create a branch and modify the relevant Helm charts
   2. Submit a pull request
   3. After merge to main, GitHub Actions will:
      - Lint and validate changes
      - Deploy updates to the cluster
      - Ensure zero-downtime deployments with rolling updates

4. **Monitoring Deployments**
   - Track deployment status in GitHub Actions
   - View deployment history using:
     ```bash
     helm history <chart-name>
     ```
   - Rollback if needed:
     ```bash
     helm rollback <chart-name> <revision>
     ```

### Security Considerations
- Kubernetes credentials are stored securely as GitHub Secrets
- All configuration changes require pull request approval
- Helm charts are version controlled and changes are tracked