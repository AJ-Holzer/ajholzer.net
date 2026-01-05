# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import requests  # type: ignore[import-untyped]
import time

from pprint import pprint
from config import config
from typing import Any, Optional
from integrations.github.types import GithubProject


class GithubFetcher:
    def __init__(self) -> None:
        self.__HEADERS: dict[str, str] = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        }

        # Store last update time
        self.__last_updated: Optional[float] = None

        # Store projects for the given interval
        self.__projects: list[GithubProject] = []

    def __get_repos(self) -> list[GithubProject]:
        """Fetch all repositories, sort by creation date descending, then take the configured max number."""
        query: str = f"""
        {{
            user(login: "{config.GITHUB_USERNAME}") {{
                repositories(first: 100, isFork: false) {{
                    nodes {{
                        name
                        url
                        description
                        updatedAt
                        defaultBranchRef {{
                            target {{
                                ... on Commit {{
                                    history {{
                                        totalCount
                                    }}
                                }}
                            }}
                        }}
                    }}
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                }}
            }}
        }}
        """

        all_repos: list[dict[str, Any]] = []
        has_next_page = True
        end_cursor: Optional[str] = None

        # Paginate through all repos
        while has_next_page:
            paged_query = query
            if end_cursor:
                paged_query = f"""
                {{
                    user(login: "{config.GITHUB_USERNAME}") {{
                        repositories(first: 100, after: "{end_cursor}", isFork: false) {{
                            nodes {{
                                name
                                url
                                description
                                updatedAt
                                defaultBranchRef {{
                                    target {{
                                        ... on Commit {{
                                            history {{
                                                totalCount
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                            pageInfo {{
                                hasNextPage
                                endCursor
                            }}
                        }}
                    }}
                }}
                """
            response: requests.Response = requests.post(
                "https://api.github.com/graphql",
                json={"query": paged_query},
                headers=self.__HEADERS,
            )
            response.raise_for_status()
            data = response.json()["data"]["user"]["repositories"]
            all_repos.extend(data["nodes"])
            has_next_page = data["pageInfo"]["hasNextPage"]
            end_cursor = data["pageInfo"]["endCursor"]

        # Sort all repos by creation date descending
        all_repos_sorted = sorted(all_repos, key=lambda r: r["updatedAt"], reverse=True)

        pprint(all_repos_sorted)

        # Take only the configured max number of repos
        selected_repos = all_repos_sorted[: config.GITHUB_MAX_REPOS]

        projects: list[GithubProject] = []
        for repo in selected_repos:
            commit_count = (
                repo.get("defaultBranchRef", {})
                .get("target", {})
                .get("history", {})
                .get("totalCount", 0)
            )
            projects.append(
                GithubProject(
                    url=repo["url"],
                    name=repo["name"],
                    description=repo.get("description", ""),
                    commit_count=commit_count,
                )
            )
        return projects

    @property
    def projects(self) -> list[GithubProject]:
        """Returns the most resent projects within the interval.

        Returns:
            list[GithubProject]: The Github projects.
        """
        # Get current time in seconds since the last epoch
        current_time: float = time.time()

        # Skip if projects don't need to be updated
        if (
            self.__last_updated is not None
            and self.__last_updated + config.PROJECT_EXPIRATION_INTERVAL_MINUTES * 60
            > current_time
            and self.__projects
        ):
            return self.__projects

        # Update data
        self.__projects = self.__get_repos()

        # Update last update time
        self.__last_updated = current_time

        return self.__projects
