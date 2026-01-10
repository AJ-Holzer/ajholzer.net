# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import logging

from fastapi import APIRouter
from api.models import GitProject
from api.src.integrations.github.github_interface import GitHub


logger: logging.Logger = logging.getLogger(__name__)

# Initialize router
router: APIRouter = APIRouter()
PREFIX: str = "/github"
TAGS: list[str] = ["github"]

# Initialize github fetcher
github_fetcher: GitHub = GitHub()


@router.get(path="/projects", response_model=list[GitProject])
def list_projects() -> list[GitProject]:
    """Get github projects.

    Returns:
        list[Project]: The github projects.
    """
    logger.debug("Retrieving Github projects...")
    return [
        GitProject(
            url=project.url,
            name=project.name,
            description=project.description or "",
            commit_count=project.commit_count,
        )
        for project in github_fetcher.repositories
    ]
