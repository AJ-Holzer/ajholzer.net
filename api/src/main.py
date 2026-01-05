# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from config import config
from api.app import API


def main() -> None:
    # Check config
    config.check()

    # Init api
    api: API = API()

    # Start api
    api.start()


if __name__ == "__main__":
    main()
