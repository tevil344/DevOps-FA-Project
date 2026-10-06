# FA demonstration runbook

Use this order in front of faculty. It produces visible proof at each layer.

1. Show the architecture in the root README: Terraform creates EC2, Ansible configures it, Docker Compose runs three containers.
2. In `terraform/`, show `terraform validate` and `terraform plan`; point to SSH restricted by `admin_cidr`, HTTP port 80, encrypted root disk, and IMDSv2.
3. Show the EC2 instance as running in AWS, then update `ansible/inventory.ini` with its public IP.
4. Run `ansible ... -m ping`, followed by the playbook. Explain idempotency: re-running converges the server to the declared state.
5. On the EC2 host, show `docker compose ps` and `docker compose logs --tail=30 backend`.
6. Open `http://EC2_PUBLIC_IP/api/health/` and the browser UI.
7. Show `docker-compose.yml`: frontend is the only published service; database and Django API are isolated on Docker's internal network.
8. Finish by showing the four files in `docs/` that answer the viva and team questions.

Local fallback: use `docker compose up --build -d`, open `http://localhost`, and run `curl http://localhost/api/health/`.
