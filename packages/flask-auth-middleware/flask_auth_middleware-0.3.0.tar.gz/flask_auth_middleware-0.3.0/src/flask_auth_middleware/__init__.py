__version__ = "0.3.0"

from .auth_middleware import JWTAuthMiddleware as JWTAuthMiddleware
from .auth_decorator import login_required as login_required
