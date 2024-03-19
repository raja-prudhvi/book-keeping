
# Book-Keeping App

A general-purpose book-keeping application designed to demonstrate the integration of an application with Kubernetes and Google Cloud Platform (GCP) services. The infrastructure code is managed using Terraform.

**Note:** `bookkeeping.public.io` is provisioned via Terraform modules, integrating Cloud Armor WAF rules and DDoS mitigation through GCLB ingress.

## Architecture Overview

### Via GCLB Ingress

```
User Request (bookkeeping.public.io)
↓ [Ingress: book-keeping-ingress (Port 80)]
↓ [Service: book-keeping (Port 80 → TargetPort 5000)]
↓ [Pod: book-keeping-app (ContainerPort 5000)]
```

### Via Istio Ingress

```
User hits bookkeeping.public.io
→ DNS resolves to Istio Ingress Gateway IP
→ Istio Gateway (book-keeping-gateway) receives the request
→ Istio VirtualService (bookkeeping-virtualservice) matches the request and routes it
→ Kubernetes Service (book-keeping-service) directs the request to the correct pod
→ Request reaches book-keeping-app container on port 5000
```

### ExternalDNS Integration

Integrates with ExternalDNS to automatically update DNS records to point to Istio's Ingress Gateway, simplifying the routing of external traffic to the correct services within the cluster.

## Project Structure

```plaintext
.
├── Dockerfile
├── README.md
├── app.py
├── istio-ingress-app
│   ├── .docker/ghcr_config.json
│   ├── db-credentials-secret.yaml
│   ├── deployment.yaml
│   ├── ghcr_secret.yaml
│   ├── gke_ingress.yaml
│   ├── istio_gateway.yaml
│   ├── istio_virtualservice.yaml
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   └── service.yaml
├── requirements.txt
└── templates
    └── index.html
```

## Generating Sensitive Files

Before deploying the application, generate the following secret files with your specific credentials. These files contain sensitive information and should not be committed to version control. 
PS : I have addded some dummy values in sensitive files, so u can understand how it will actually look like below.

### Database Credentials (`db-credentials-secret.yaml`)

1. Encode your database credentials (username, password, host, port, and database name) in base64.
2. Create `db-credentials-secret.yaml` with the base64-encoded values.
3. echo -n 'db_user_value' | base64 --> do the same for all the values below individually inorder to get base64 value

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: book-keeping-app
type: Opaque
data:
  DB_USER: base64_encoded_username
  DB_PASSWORD: base64_encoded_password
  DB_HOST: base64_encoded_host
  DB_PORT: base64_encoded_port
  DB_NAME: base64_encoded_database_name
```

### GitHub Container Registry Secret (`ghcr_secret.yaml`)

1. Create a `.docker/ghcr_config.json` file with your GHCR credentials encoded in base64.
2. Encode the entire `.docker/ghcr_config.json` file in base64.
3. Create `ghcr_secret.yaml` using the base64-encoded `.docker/ghcr_config.json`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ghcr-login-credentials
  namespace: book-keeping-app
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: base64_encoded_ghcr_config.json
```

### GHCR Configuration (`.docker/ghcr_config.json`)

"auth" value below is the base64 encoded value of username:password, 'username' is the github username, 'password' is the github token.

```json
{
  "auths": {
    "ghcr.io": {
      "username": "your_username",
      "password": "your_password",
      "email": "your_email@example.com",
      "auth": "base64_encoded_credentials"
    }
  }
}
```

## Deployment Instructions

Deployment Instructions
Generate Sensitive Files: Ensure to generate db-credentials-secret.yaml, ghcr_secret.yaml, and .docker/ghcr_config.json. These files are added to .gitignore as they contain sensitive content.

Build and Push Docker Image: Use Docker buildx for building and pushing the image to GitHub Container Registry (GHCR).

```
docker buildx build --platform linux/amd64 -t ghcr.io/{repo_name}/book-keeping:latest --push .
```

## Deploy App on GKE Cluster:

```
cd /path/to/book-keeping
kubectl apply -k ./istio-ingress-app

```

## Access the Application

Navigate to `bookkeeping.public.io` in your web browser to access the book-keeping application.
