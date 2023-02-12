import os

from margay.sdk.auth import JWTAuth
from margay.sdk.client import Client

if __name__ == "__main__":
    app_secret = os.getenv("MARGAY_AUTH_SECRET", "SuperSecret")
    token = JWTAuth(app_secret).issue_token("JohnSnow")
    dsn = os.getenv("MARGAY_DSN", "ws://127.0.0.1:8080")
    client = Client(dsn, token)
    client.run()
