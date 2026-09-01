"""
shared/auth.py

JWT-based authentication for the CSIA backend. Every module protects its
routes the same way:

    from shared.auth import get_current_user

    @router.get("/cases/{case_id}")
    def get_case(case_id: str, user: dict = Depends(get_current_user)):
        ...

This keeps "is this person logged in?" logic in ONE place instead of every
module (case_management, evidence_upload, etc.) reinventing it.

Requires:
    pip install python-jose[cryptography] passlib[bcrypt]
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from shared.exceptions import AuthenticationError, AuthorizationError

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# In production/deployment, set this via an environment variable — never
# hardcode a real secret. This fallback is only for local dev.
SECRET_KEY = os.getenv("CSIA_SECRET_KEY", "dev-only-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8-hour login session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Points FastAPI's docs/Swagger UI at the login endpoint that issues tokens.
# Update the path if case_management/routes.py exposes login somewhere else.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(plain_password: str) -> str:
    """Hash a password before storing it. Never store plain-text passwords."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login attempt's password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# Token creation
# ---------------------------------------------------------------------------

def create_access_token(user_id: str, role: str = "investigator",
                         expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT for a logged-in user.

    Called from the login route once the username/password is verified:

        token = create_access_token(user_id=user.id, role=user.role)
        return {"access_token": token, "token_type": "bearer"}
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT. Raises AuthenticationError if invalid/expired."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise AuthenticationError("Session expired or token is invalid. Please log in again.")


# ---------------------------------------------------------------------------
# Dependencies — import these in other modules' routes.py
# ---------------------------------------------------------------------------

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    FastAPI dependency that extracts and validates the logged-in user from
    the request's Authorization header.

    Returns a dict like: {"id": "...", "role": "investigator"}
    """
    payload = decode_access_token(token)
    user_id: str = payload.get("sub")
    role: str = payload.get("role", "investigator")

    if user_id is None:
        raise AuthenticationError("Invalid token: missing user identity.")

    return {"id": user_id, "role": role}


def require_role(*allowed_roles: str):
    """
    Dependency factory for role-gated routes, e.g. only "admin" can delete
    a case, or only "lead" can export the final report.

        @router.delete("/cases/{case_id}")
        def delete_case(case_id: str, user: dict = Depends(require_role("admin"))):
            ...
    """
    def role_checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in allowed_roles:
            raise AuthorizationError(
                f"This action requires one of the following roles: {', '.join(allowed_roles)}."
            )
        return user

    return role_checker
