# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from fastapi import APIRouter


router: APIRouter = APIRouter()
PREFIX: str = "/test"
TAGS: list[str] = ["test"]


@router.get(path="", response_model=dict[str, str])
def test() -> dict[str, str]:
    return {"status": "OK"}
