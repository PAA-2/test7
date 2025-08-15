import ipaddress
import os
import threading
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

_thread_locals = threading.local()


def get_current_user():
    return getattr(_thread_locals, "user", None)


class CurrentUserMiddleware(MiddlewareMixin):
    """Expose l’utilisateur courant aux signaux (audit)."""

    def process_request(self, request):
        _thread_locals.user = getattr(request, "user", None)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Ajoute CSP et autres headers de sécurité."""

    def process_response(self, request, response):
        response["Referrer-Policy"] = settings.SECURE_REFERRER_POLICY
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = settings.X_FRAME_OPTIONS
        response["Content-Security-Policy"] = (
            f"default-src {' '.join(settings.CSP_DEFAULT_SRC)}; "
            f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}; "
            f"style-src {' '.join(settings.CSP_STYLE_SRC)}; "
            f"img-src {' '.join(settings.CSP_IMG_SRC)}; "
            f"connect-src {' '.join(settings.CSP_CONNECT_SRC)}; "
            f"frame-ancestors {' '.join(settings.CSP_FRAME_ANCESTORS)}"
        )
        return response


class AdminIPAllowlistMiddleware(MiddlewareMixin):
    """Bloque l’accès /admin et /paa/adminpanel si IP non autorisée."""

    def __init__(self, get_response=None):
        super().__init__(get_response)
        allowlist = os.environ.get("ADMIN_IP_ALLOWLIST", "")
        self.networks = []
        for cidr in [c.strip() for c in allowlist.split(",") if c.strip()]:
            try:
                self.networks.append(ipaddress.ip_network(cidr, strict=False))
            except ValueError:
                pass

    def _allowed(self, ip):
        if not self.networks:
            return True
        try:
            addr = ipaddress.ip_address(ip)
            return any(addr in net for net in self.networks)
        except ValueError:
            return False

    def process_request(self, request):
        path = request.path or ""
        if path.startswith("/admin") or path.startswith("/paa/adminpanel"):
            ip = (
                request.META.get("REMOTE_ADDR")
                or request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
            )
            if not self._allowed(ip):
                return HttpResponseForbidden("IP non autorisée pour l’administration.")
