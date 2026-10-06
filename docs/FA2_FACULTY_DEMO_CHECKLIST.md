# FA2 faculty demonstration checklist

Use this as the live script. Complete each checkbox before the demonstration.

## Before the session

- [ ] Replace the four `<name>` placeholders in `TEAM_CONTRIBUTIONS.md` and the title slide.
- [ ] Push the final project to the group GitHub repository.
- [ ] Confirm the **CI** workflow passes on the commit being demonstrated.
- [ ] Create the GitHub `production` environment and add the three secrets from `FA2_CICD.md`.
- [ ] Fill `.env` with strong local demo passwords. Do not show it on screen.
- [ ] Set `OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318` in `.env` for the trace demo.
- [ ] Start the local monitoring stack:

  ```bash
  docker compose --profile observability up --build -d
  ```

- [ ] Check `curl http://localhost/api/health/` returns a healthy response.
- [ ] Open these tabs before faculty arrives: GitHub Actions, application, Prometheus Targets, Grafana, Jaeger.

## During the session

- [ ] State the CropLeaf reliability problem and DevOps goal.
- [ ] Show the architecture slide and repository folders.
- [ ] Show the CI workflow: Python syntax, unit tests, React build, Docker build, Compose validation, Trivy scan.
- [ ] Show a successful workflow run from the current commit.
- [ ] Start the protected CD workflow and explain that GitHub approval precedes deployment.
- [ ] Show Ansible ping/playbook output and its health-check task.
- [ ] Open the deployed CropLeaf UI and `/api/health/`.
- [ ] Open Prometheus Targets and show `cropleaf-backend` as UP.
- [ ] Open Grafana dashboard and generate a few health/UI requests so the charts update.
- [ ] In Grafana Explore, select Loki and query `{container=~".*backend.*"}`.
- [ ] Open Jaeger, select `cropleaf-backend`, and show a health-request trace.
- [ ] Show the two Prometheus alert rules, SLO, error budget, and incident runbook.
- [ ] Show Kubernetes manifests and explain readiness probes plus rolling update.

## Evidence to save

- [ ] Green GitHub CI run with unit-test output.
- [ ] CD approval and Ansible deployment output.
- [ ] Browser application plus health endpoint response.
- [ ] Prometheus Target page showing UP.
- [ ] Grafana dashboard, Loki log query, and Jaeger trace.
- [ ] Kubernetes `kubectl get all -n cropleaf` or rendered manifest output.

## Two-minute viva fallback

If time is short, show: the green CI run, `docker compose ps`, `/api/health/`, Prometheus target UP, Grafana overview, and the `backend.yaml` rolling-update/probe section. Then point to `FA2_RUBRIC_COVERAGE.md` for the full mapping.
