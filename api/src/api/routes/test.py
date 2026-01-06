# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import logging

from fastapi import APIRouter


logger: logging.Logger = logging.getLogger(name=__name__)

# Initialize router
router: APIRouter = APIRouter()
PREFIX: str = "/test"
TAGS: list[str] = ["test"]


@router.get(path="", response_model=dict[str, str])
def test() -> dict[str, str]:
    logger.debug("API test successful!")
    return {"status": "OK"}
