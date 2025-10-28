# ci-cd-pipeline-demo

Lightweight demo showing a CI/CD pipeline:
- CI: GitHub Actions builds container image and pushes to Docker Hub.
- CD: Argo CD deploys the application to a Kubernetes cluster.

## Features
- Build and push Docker image from GitHub Actions.
- Deploy via Argo CD to any Kubernetes cluster.
- Example Helm/manifest-based Argo CD Application configuration included.

## Prerequisites
- Git, Docker, kubectl configured for your cluster
- Helm v3
- Docker Hub account and repository
- GitHub repository with Actions enabled
- (Optional) Argo CD CLI (argocd) for convenience

## Repository layout (recommended)
- .github/workflows/ci.yml        # GitHub Actions workflow that builds & pushes image
- k8s/                           # Kubernetes manifests / Helm chart
- argocd/                         # Argo CD Application manifests (optional)
- README.md

## CI (GitHub Actions) — high level
1. Workflow triggered on push (or tags).
2. Build Docker image (tag with git SHA or semantic tag).
3. Login to Docker Hub using secrets and push image.

Required GitHub Secrets:
- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN (or password)
- IMAGE_NAME (optional)

## CD (Argo CD) — install and usage

Prerequisites: kubectl configured to target your Kubernetes cluster, Helm v3 installed.

1. Add Argo Helm repo and update:
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

2. Create namespace:
```bash
kubectl create namespace argocd
```

3. Create a values file `argocd-values.yaml` with the following content:
```yaml
server:
    service:
        type: NodePort
        nodePort: 30007
    ingress:
        enabled: false
configs:
    params:
        server.insecure: true
```

4. Install Argo CD using Helm:
```bash
helm install argocd argo/argo-cd -n argocd -f argocd-values.yaml
```

5. Verify pods and Helm release:
```bash
kubectl get pods -n argocd
helm list -n argocd
```

Access:
- Because server.service.type=NodePort and nodePort=30007, access Argo CD UI at:
    - kubectl port-forward svc/argocd-server -n argocd 8080:443
    - Visit: https://localhost:8080
- Initial admin password (if using default install):
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
Use username `admin` and the password above (or configure your own).

## Notes & tips
- Keep CI secrets secure in GitHub repository settings.
- Use immutable tags (SHA) to avoid deployment drift.
- Configure health checks and resource limits in k8s manifests.
- For production, use TLS and a proper ingress or load balancer instead of NodePort and avoid server.insecure=true.

## Troubleshooting
- Check Argo CD server and controller logs:
```bash
kubectl logs -n argocd deployment/argocd-server
kubectl logs -n argocd deployment/argocd-application-controller
```
- Verify image exists in Docker Hub and tag matches what Argo CD expects.