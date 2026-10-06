"""Low-cardinality HTTP metrics for Prometheus and the FA2 SRE demonstration."""
import time

from prometheus_client import Counter, Histogram

REQUESTS = Counter(
    'cropleaf_http_requests_total',
    'HTTP responses served by CropLeaf',
    ['method', 'path', 'status'],
)
LATENCY = Histogram(
    'cropleaf_http_request_duration_seconds',
    'Time spent serving CropLeaf HTTP requests',
    ['method', 'path'],
)


def metric_path(request):
    """Avoid unbounded labels caused by user-supplied URL values."""
    if request.path.startswith('/api/predict/'):
        return '/api/predict/'
    if request.path.startswith('/api/health/'):
        return '/api/health/'
    if request.path.startswith('/api/auth/'):
        return '/api/auth/'
    if request.path == '/metrics':
        return '/metrics'
    return 'other'


class PrometheusMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = time.monotonic()
        response = self.get_response(request)
        path = metric_path(request)
        REQUESTS.labels(request.method, path, response.status_code).inc()
        LATENCY.labels(request.method, path).observe(time.monotonic() - started)
        return response
