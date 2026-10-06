# FA2 rubric coverage checklist

## Problem statement

**CropLeaf reliable delivery and observability platform:** Farmers need a dependable crop-disease detection web application. Manual deployment risks inconsistent environments, long outage recovery, and no visibility into failures. This project automates build, test, containerization, provisioning, deployment, monitoring, logging, alerting, and recovery evidence for CropLeaf.

## Pipeline mapping - 8 marks

| FA2 rubric requirement | Implemented evidence | Demonstration proof |
|---|---|---|
| Source | GitHub repository, pull-request workflow | Show commits/PR and Actions trigger |
| Build | React production build and Docker image build in CI | Green **CI** job logs |
| Test | `tests/test_observability.py` unit tests run in CI | Unit-test output in Actions |
| Containerization | Backend and frontend Dockerfiles, Compose | `docker compose images` / CI build log |
| Deployment | Terraform, Ansible, EC2 Compose; Kubernetes alternative | Ansible playbook and `/api/health/` output |
| Monitoring | Prometheus, Grafana, health/readiness checks, alert rules | Prometheus Targets + Grafana dashboard |
| Centralized logs | Promtail collects Docker logs into Loki, queried in Grafana | Grafana Explore Loki query |
| SRE | SLO, error budget, incident runbooks, rolling update | `SRE_RUNBOOK.md`, Kubernetes manifests |

## Tools mapped to Unit III and Unit IV

| Syllabus concept | CropLeaf implementation |
|---|---|
| CI/CD pipeline as code | GitHub Actions YAML in `.github/workflows/` |
| Automated build and unit test | CI workflow: Python compile, unit test, Vite build |
| DevSecOps | Trivy Infrastructure-as-Code scan; secrets excluded from Git; protected production environment |
| Continuous delivery and deployment strategy | Approval-gated CD; Ansible health verification; Kubernetes RollingUpdate manifests |
| Container orchestration | Kubernetes namespace, Deployment, StatefulSet, Service, Ingress, probes and resource limits |
| Metrics and visualization | Prometheus scrape and Grafana dashboard |
| Logs | Docker -> Promtail -> Loki -> Grafana Explore |
| Traces | OpenTelemetry Django instrumentation -> Jaeger |
| SRE | 99% weekly availability SLO, error budget, alerts, incident runbooks |

## Faculty demonstration sequence

1. Explain the problem statement and show this table.
2. Push a small safe change and show CI stages go green.
3. Trigger the protected CD workflow for that tested commit; show Ansible and post-deploy health validation.
4. Generate normal UI/health traffic, then show Prometheus **UP** and Grafana request/latency panels.
5. Show the Loki log query and the alert rules.
6. Show the Kubernetes manifests and explain rolling update/readiness probes.

Fill the four actual team names in `TEAM_CONTRIBUTIONS.md` and retain screenshots of all six steps before submission.
