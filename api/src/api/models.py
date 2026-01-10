# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from pydantic import BaseModel


class GitHubRepositoryModel(BaseModel):
    url: str
    name: str
    description: str
    commit_count: int
