"""Azure AD authentication helpers for Streamlit.

This module wraps the MSAL client so the main app can request an auth code
flow, exchange the callback parameters for a token, and read ID token claims
for the signed-in user.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List

import msal
import streamlit as st


class AuthConfigurationError(RuntimeError):
    """Raised when the Azure AD configuration is incomplete."""


@dataclass
class AuthConfig:
    """Configuration needed to talk to Azure AD."""

    client_id: str
    tenant_id: str
    client_secret: str
    redirect_uri: str
    scopes: List[str]

    @property
    def authority(self) -> str:
        return f"https://login.microsoftonline.com/{self.tenant_id}"


class AzureAuthManager:
    """Handles Azure AD login flows using MSAL."""

    def __init__(self, config: AuthConfig):
        self.config = config
        self.client = msal.ConfidentialClientApplication(
            client_id=config.client_id,
            client_credential=config.client_secret,
            authority=config.authority,
        )

    def build_authorization_url(self, state: str | None = None) -> str:
        """Return the Microsoft login URL for interactive auth."""
        return self.client.get_authorization_request_url(
            scopes=self.config.scopes,
            redirect_uri=self.config.redirect_uri,
            state=state,
        )

    def exchange_code_for_token(self, auth_code: str) -> Dict:
        """Exchange an auth code for a token set."""
        return self.client.acquire_token_by_authorization_code(
            auth_code,
            scopes=self.config.scopes,
            redirect_uri=self.config.redirect_uri,
        )

ENV_CLIENT_ID = "AZURE_CLIENT_ID"
ENV_TENANT_ID = "AZURE_TENANT_ID"
ENV_CLIENT_SECRET = "AZURE_CLIENT_SECRET"
ENV_REDIRECT_URI = "AZURE_REDIRECT_URI"



def _get_setting(env_var: str, secret_key: str) -> str:
    """Read a configuration value from env vars or Streamlit secrets."""

    env_value = (os.getenv(env_var) or "").strip()
    if env_value:
        return env_value

    try:
        secrets = st.secrets
    except (RuntimeError, AttributeError):
        secrets = {}

    candidates = [secret_key, env_var]

    grouped = secrets.get("azure", {})
    for key in candidates:
        value = str(grouped.get(key, "")).strip()
        if value:
            return value

    for key in candidates:
        value = str(secrets.get(key, "")).strip()
        if value:
            return value

    return ""


def load_auth_config() -> AuthConfig:
    """Load Azure AD configuration from environment variables.

    Required variables:
    * AZURE_CLIENT_ID
    * AZURE_TENANT_ID
    * AZURE_CLIENT_SECRET
    * AZURE_REDIRECT_URI
    """

    client_id = _get_setting(ENV_CLIENT_ID, "client_id")
    tenant_id = _get_setting(ENV_TENANT_ID, "tenant_id")
    client_secret = _get_setting(ENV_CLIENT_SECRET, "client_secret")
    redirect_uri = _get_setting(ENV_REDIRECT_URI, "redirect_uri")

    if not all([client_id, tenant_id, client_secret, redirect_uri]):
        missing = [
            name
            for name, value in (
                (ENV_CLIENT_ID, client_id),
                (ENV_TENANT_ID, tenant_id),
                (ENV_CLIENT_SECRET, client_secret),
                (ENV_REDIRECT_URI, redirect_uri),
            )
            if not value
        ]
        raise AuthConfigurationError(
            "Missing Azure AD configuration: " + ", ".join(missing)
        )

    return AuthConfig(
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scopes=["User.Read"],
    )
