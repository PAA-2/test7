import time
import uuid
import structlog
from django.utils.deprecation import MiddlewareMixin
from prometheus_client import Histogram, Counter

logger = structlog.get_logger(__name__)

REQ_TIME = Histogram(
    "paa_http_request_seconds", "HTTP request latency (s)", ["path", "method", "status"]
)
REQ_COUNT = Counter(
    "paa_http_requests_total", "HTTP requests", ["path", "method", "status"]
)


class RequestIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        req_id = request.META.get("HTTP_X_REQUEST_ID") or str(uuid.uuid4())
        request.request_id = req_id
        structlog.contextvars.bind_contextvars(request_id=req_id)

    def process_response(self, request, response):
        response["X-Request-ID"] = getattr(request, "request_id", "")
        return response


class AccessLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._t0 = time.time()

    def process_response(self, request, response):
        try:
            dur = time.time() - getattr(request, "_t0", time.time())
            path = request.path.split("?")[0]
            status = str(response.status_code)
            method = request.method
            REQ_TIME.labels(path, method, status).observe(dur)
            REQ_COUNT.labels(path, method, status).inc()
            logger.info(
                "http_access",
                path=path,
                method=method,
                status=int(status),
                duration_ms=int(dur * 1000),
            )
        except Exception:
            pass
        return response
