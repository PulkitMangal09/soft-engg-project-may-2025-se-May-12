# app/config.py
import os
from typing import Optional

from dotenv import load_dotenv
import httpx
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: Optional[str] = (
    os.getenv("NEXT_PUBLIC_SUPABASE_URL")
)

SUPABASE_SERVICE_ROLE_KEY: Optional[str] = (os.getenv("NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY")
)
    
SUPABASE_ANON_KEY: Optional[str] = (
 os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
)

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not set in environment")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is not set in environment")

# ─────────────────────────────────────────────────────────────
# HTTP client: disable HTTP/2 to avoid intermittent disconnects
# ─────────────────────────────────────────────────────────────
_http = httpx.Client(http2=False, timeout=30.0)

# Create the global Supabase client (service role for backend operations)
def _make_service_client() -> Client:
    """
    Build a Supabase client using the service-role key.
    We try to pass our custom httpx client; if the installed supabase-py
    version doesn't support that kwarg yet, we patch the postgrest session.
    """
    try:
        # Some versions accept http_client= directly
        client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, http_client=_http)  # type: ignore[arg-type]
        return client
    except TypeError:
        # Older versions: create first, then patch the postgrest session
        client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        try:
            # postgrest client exposes a .session which is an httpx Client
            client.postgrest.client.session = _http  # type: ignore[attr-defined]
        except Exception:
            # If patching fails we still return a working client; only HTTP/2 fix is skipped
            pass
        return client

supabase: Client = _make_service_client()

# ─────────────────────────────────────────────────────────────
# Optional helper: make a per-request client that enforces RLS
# (queries run "as the user" using their JWT). Handy when you
# don't want to rely on service role for a route.
# ─────────────────────────────────────────────────────────────
def make_user_rls_client(user_jwt: str) -> Client:
    """
    Create a short-lived Supabase client that authenticates PostgREST
    requests with the user's JWT (RLS context).
    """
    if not SUPABASE_ANON_KEY:
        raise RuntimeError("SUPABASE_ANON_KEY missing; cannot create RLS client")
    try:
        client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY, http_client=_http)  # type: ignore[arg-type]
    except TypeError:
        client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        try:
            client.postgrest.client.session = _http  # type: ignore[attr-defined]
        except Exception:
            pass

    # Tell PostgREST to use the user's token for RLS
    try:
        client.postgrest.auth(user_jwt)  # type: ignore[attr-defined]
    except Exception:
        # Older versions use different attribute names; silently ignore if missing
        pass
    return client
