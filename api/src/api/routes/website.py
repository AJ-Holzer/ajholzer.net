# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import subprocess
import hmac
import hashlib

from fastapi import APIRouter, HTTPException, Request
from config import config


router: APIRouter = APIRouter()
PREFIX: str = "/website"
TAGS: list[str] = ["website"]

# Path to your website Git repository
REPO_PATH: str = "/var/www/html/ajholzer.net"

COMMANDS: list[list[str]] = [
    ["git", "-C", REPO_PATH, "reset", "--hard", "HEAD"],
    ["git", "-C", REPO_PATH, "clean", "-fd"],
    ["git", "-C", REPO_PATH, "pull", "origin", "main"],
    ["sudo", "systemctl", "restart", "api.ajholzer.net"],
]


@router.post(path="/update-site", response_model=dict[str, str])  # type: ignore
async def update_site(request: Request) -> dict[str, str]:
    """Update the website hosted at ajholzer.net.

    Raises:
        HTTPException: When the update fails.

    Returns:
        dict[str, str]: When the update was successfully.
    """
    # Get the signature header from GitHub
    signature = request.headers.get("X-Hub-Signature-256")
    if signature is None:
        raise HTTPException(status_code=403, detail="Missing signature")

    # Read the raw body for signature verification
    body = await request.body()

    # Compute HMAC with the secret
    mac = hmac.new(config.GITHUB_WEBSITE_SECRET, msg=body, digestmod=hashlib.sha256)
    expected_signature = f"sha256={mac.hexdigest()}"

    # Compare the signature
    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Optional: check event type if you want
    event_type = request.headers.get("X-GitHub-Event")
    if event_type != "push":
        raise HTTPException(status_code=400, detail="Not a push event")

    try:
        print("🟠 Updating site data for ajholzer.net...")

        # Run commands
        for command in COMMANDS:
            subprocess.run(
                args=command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        return {
            "status": "success",
            "message": "Site updated",
        }
    except subprocess.CalledProcessError as exc:
        if exc.stdout:
            print(exc.stdout.decode())
        if exc.stderr:
            print(exc.stderr.decode())

        raise HTTPException(
            status_code=500,
            detail="Update failed",
        )
