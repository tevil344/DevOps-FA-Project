# CropLeaf - DevOps FA1 and FA2 Project

CropLeaf identifies crop-leaf diseases through a Django API and React user interface. The project delivers a complete FA1 and FA2 DevOps implementation: repeatable local containers, AWS provisioning, automated configuration, CI/CD, Kubernetes manifests, monitoring, logging, tracing, and SRE evidence.

```text
Developer -> Terraform -> AWS EC2 -> Ansible -> Docker Compose -> CropLeaf -> Browser
```

## What is included

| Layer | Deliverable | Responsibility |
|---|---|---|
| Application | Django API + React UI | Login, images, predictions, dashboard |
| Docker | `docker-compose.yml`, two Dockerfiles, Nginx proxy | Same application stack on every machine |
| Terraform | `terraform/` | EC2, security group, encrypted disk, IMDSv2 |
| Ansible | `ansible/deploy.yml` | Installs Docker and deploys the chosen Git revision |
| Security | `.env.example`, protected Ansible template, hardened settings | Keeps credentials out of Git and limits network access |
| CI/CD | `.github/workflows/` | Validates every change and deploys approved revisions |
| Observability | `monitoring/` | Prometheus metrics, Grafana dashboard, SRE alerts and runbook |
| Orchestration | `k8s/` | Kubernetes workload, storage, probes, ingress and rolling updates |

## Assessment deliverables

- FA1 viva preparation: [docs/VIVA.md](docs/VIVA.md)
- FA2 rubric mapping: [docs/FA2_RUBRIC_COVERAGE.md](docs/FA2_RUBRIC_COVERAGE.md)
- Faculty demonstration checklist: [docs/FA2_FACULTY_DEMO_CHECKLIST.md](docs/FA2_FACULTY_DEMO_CHECKLIST.md)
- Presentation deck: [docs/CropLeaf_FA2_DevOps_Presentation.pptx](docs/CropLeaf_FA2_DevOps_Presentation.pptx)

## Local demonstration with Docker

Prerequisite: Docker Desktop.

```bash
cp .env.example .env
# Edit .env: set strong POSTGRES_PASSWORD and SECRET_KEY values.
docker compose up --build -d
docker compose ps
curl http://localhost/api/health/
```

Open `http://localhost`. Stop it with `docker compose down`; add `-v` only when you intentionally want to delete the database and uploaded files.

The ML files are intentionally not committed. Add secure HTTPS model URLs or Google Drive IDs to `.env` if you want image prediction; the rest of the application and health endpoint start without them.

## AWS + Ansible demonstration

1. Create an EC2 key pair named `fa1-key` and save its PEM outside this repository. Restrict the PEM: `chmod 400 ../fa1-key.pem`.
2. Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars`, set your key name and public IP `/32`, then run:

   ```bash
   cd terraform
   terraform init
   terraform fmt -check
   terraform validate
   terraform plan
   terraform apply
   ```

3. Copy `ansible/inventory.ini.example` to `ansible/inventory.ini` and replace the host IP. Copy `ansible/group_vars/all.yml.example` to `ansible/group_vars/all.yml`, set the values, then encrypt that real vars file:

   ```bash
   ansible-galaxy collection install -r ansible/collections/requirements.yml
   ansible-vault encrypt ansible/group_vars/all.yml
   ansible -i ansible/inventory.ini cropleaf -m ping
   ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-vault-pass
   ```

4. Visit `http://EC2_PUBLIC_IP/api/health/`, then `http://EC2_PUBLIC_IP`.
5. After assessment, run `terraform destroy` from `terraform/` to avoid cloud charges.

Before the Ansible step, push this FA-ready repository to your own GitHub repository or set `app_repo` to the repository containing these DevOps files. Ansible checks out exactly `app_version`, making deployments repeatable.

## Assessment guide

Use [docs/VIVA.md](docs/VIVA.md) for short answers and exact file locations, [docs/RUNBOOK.md](docs/RUNBOOK.md) for your live demonstration order, and [docs/TEAM_CONTRIBUTIONS.md](docs/TEAM_CONTRIBUTIONS.md) to fill your real four-member responsibilities.

## FA2: CI/CD, monitoring and SRE

The FA2 implementation is documented in [docs/FA2_RUBRIC_COVERAGE.md](docs/FA2_RUBRIC_COVERAGE.md), [docs/FA2_CICD.md](docs/FA2_CICD.md), [docs/SRE_RUNBOOK.md](docs/SRE_RUNBOOK.md), and [docs/KUBERNETES_GUIDE.md](docs/KUBERNETES_GUIDE.md). Start the complete local observability stack with:

```bash
cp .env.example .env
docker compose --profile observability up --build -d
```

This adds internal Prometheus scraping and a local-only Grafana dashboard. For CI/CD evidence, push the project to your group GitHub repository, configure the three protected deployment secrets listed in `FA2_CICD.md`, then show the Actions runs, Prometheus target state, and Grafana dashboard to faculty.
