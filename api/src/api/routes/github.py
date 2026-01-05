# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from fastapi import APIRouter
from api.models import Project
from integrations.github.fetcher import GithubFetcher


router: APIRouter = APIRouter()
PREFIX: str = "/github"
TAGS: list[str] = ["github"]

# Initialize github fetcher
github_fetcher: GithubFetcher = GithubFetcher()


@router.get(path="/projects", response_model=list[Project])
def list_projects() -> list[Project]:
    """Get github projects.

    Returns:
        list[Project]: The github projects.
    """
    return [
        Project(
            url=project.url,
            name=project.name,
            description=project.description or "",
            commit_count=project.commit_count,
        )
        for project in github_fetcher.projects
    ]
