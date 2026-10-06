# Kubernetes deployment option - Unit III

The primary assessment deployment remains Terraform + Ansible + Docker Compose on EC2. This folder additionally demonstrates Kubernetes architecture and a rolling-update strategy required by Unit III. It is designed for a local `kind`/Minikube cluster or a managed cluster after replacing the image names.

## Resources included

| Manifest | Role |
|---|---|
| `namespace.yaml` | Isolates CropLeaf resources |
| `configmap.yaml` and secret | Separates non-secret configuration from credentials |
| `postgres.yaml` | Stateful database with persistent storage claim and readiness probe |
| `backend.yaml` | Two-replica API deployment with rolling update, health probes, and resource limits |
| `frontend.yaml` | Two-replica Nginx UI deployment |
| `ingress.yaml` | Routes `cropleaf.local` to the UI |

## Demo steps

1. Build and push the two Docker images to a registry your cluster can pull from. Replace `REPLACE_WITH_YOUR_ORG` and `REPLACE_WITH_TAG` in `backend.yaml` and `frontend.yaml`.
2. Copy `k8s/secret.example.yaml` to `k8s/secret.yaml`, replace every secret, then apply it separately:

   ```bash
   kubectl apply -f k8s/namespace.yaml
   kubectl apply -f k8s/secret.yaml
   kubectl apply -k k8s/
   kubectl get all -n cropleaf
   kubectl rollout status deployment/backend -n cropleaf
   ```

3. For a local ingress controller, map `cropleaf.local` to the cluster ingress address in your hosts file. Verify the health endpoint through the service or ingress.

```bash
kubectl port-forward -n cropleaf svc/backend 8000:8000
curl http://localhost:8000/api/health/
```

Kubernetes is not deployed simultaneously with the EC2 Compose stack; select one runtime for a particular demonstration to avoid duplicate database/application costs.
