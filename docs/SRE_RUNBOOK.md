# CropLeaf monitoring, observability and SRE

## What we observe

The backend emits Prometheus metrics at an internal-only `/metrics` endpoint. The Nginx public proxy returns 404 for that endpoint, while Prometheus scrapes `backend:8000` over the Docker network. Docker container logs are collected by Promtail and sent to Loki; Grafana provides one place to inspect both metrics and centrally collected logs. OpenTelemetry automatically creates HTTP spans and exports them to Jaeger when its endpoint is configured.

| Signal | Metric / check | Why it matters |
|---|---|---|
| Availability | `up{job="cropleaf-backend"}` and `/api/health/` | Detects a backend or database failure |
| Traffic | `cropleaf_http_requests_total` | Shows demand and status codes |
| Errors | 5xx fraction from request counter | Signals user-visible failure |
| Latency | `cropleaf_http_request_duration_seconds` p95 | Shows slow requests before total outage |
| Container state | `docker compose ps` | Confirms each deployed component is running |
| Centralized logs | Loki datasource in Grafana, label `container` | Correlates backend/database messages without SSH-ing into every container |
| Traces | OpenTelemetry HTTP spans in Jaeger | Follows a request duration and status across instrumented services |

## Local monitoring demonstration

```bash
cp .env.example .env
# For the full three-pillar demonstration, set this in .env:
# OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318
docker compose --profile observability up --build -d
curl http://localhost/api/health/
```

Open Grafana at `http://localhost:3000` using the credentials in `.env`. Open Prometheus at `http://localhost:9090/targets` and show the `cropleaf-backend` target as **UP**. In Grafana Explore, select the Loki datasource and query `{container=~".*backend.*"}` to show centralized backend logs. Open Jaeger at `http://localhost:16686`, choose `cropleaf-backend`, and search after calling the health endpoint to show an HTTP trace. Grafana, Prometheus, and Jaeger are bound to `127.0.0.1`, so they are not publicly exposed by the Docker configuration.

Promtail reads Docker's local log files and socket, which is appropriate for the single-host EC2 demo. On Docker Desktop for macOS, that host path may not be mounted by the VM; the metrics/dashboard demonstration remains available, while the centralized-log proof should be shown on the Linux EC2 deployment.

The dashboard shows availability, request rate, error rate, and p95 latency. Prometheus evaluates two alert rules: backend down for one minute, and 5xx rate above 5% for five minutes.

## SLO and error budget

For the FA2 demonstration, the service-level objective is **99% successful backend availability per assessment week**. This allows an error budget of 1% of the week (100.8 minutes). The target is intentionally modest for a student demo; a production service would define SLOs from real user expectations.

## Incident runbooks

### Backend down

1. Check `http://localhost:9090/targets` and `docker compose ps`.
2. Inspect the relevant logs: `docker compose logs --tail=100 backend` and `docker compose logs --tail=100 db`.
3. Call `curl http://localhost/api/health/`. If the database is not connected, check the database container and `.env` values.
4. Recover with `docker compose up -d backend db`; verify the health endpoint and Prometheus target return to UP.
5. Record the time, cause, command used, and preventive action in the incident log.

### High 5xx rate

1. Check the Grafana error-rate and p95-latency panels to identify timing.
2. Inspect backend logs around that time; never paste passwords or `.env` values into an incident ticket.
3. Roll back to the previously known-good Git revision through the protected CD workflow, or run Ansible with that revision.
4. Confirm `/api/health/`, normal login, and a safe prediction request work before closing the incident.

## Evidence to collect for FA2

- Screenshot of a green CI run.
- Screenshot of the CD approval/deploy job and Ansible output.
- Prometheus Targets showing CropLeaf as UP.
- Grafana dashboard after generating a few requests.
- Alert rules page and this incident runbook.
