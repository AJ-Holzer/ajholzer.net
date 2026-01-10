# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from pydantic import BaseModel


class GitHubRepositoryModel(BaseModel):
    """The GitHub repository containing the url, name, description and the commit count."""

    url: str
    name: str
    description: str
    commit_count: int
