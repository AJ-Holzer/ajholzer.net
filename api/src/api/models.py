# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from pydantic import BaseModel


class GitProject(BaseModel):
    url: str
    name: str
    description: str
    commit_count: int
