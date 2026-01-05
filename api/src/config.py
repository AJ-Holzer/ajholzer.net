# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import os
import dotenv

from typing import Optional


class Config:
    def __init__(self) -> None:
        """Loads the .env and .config file."""
        # Load .env file
        dotenv.load_dotenv(dotenv_path="../../../.env")

        print(f"Looking for .env file in '{os.path.abspath('../../../.env')}'")

        # Define github config
        self.GITHUB_TOKEN: Optional[str] = os.getenv(key="GITHUB_TOKEN")
        self.GITHUB_USERNAME: Optional[str] = os.getenv(key="GITHUB_USERNAME")
        self.GITHUB_MAX_REPOS: int = int(os.getenv(key="GITHUB_MAX_REPOS", default=20))
        self.GITHUB_WEBSITE_SECRET: bytes = os.getenv(
            key="GITHUB_WEBSITE_SECRET",
            default="",
        ).encode()

        # Expiration config
        self.PROJECT_EXPIRATION_INTERVAL_MINUTES: int = int(
            os.getenv(
                key="PROJECT_EXPIRATION_INTERVAL_MINUTES",
                default=60,
            )
        )

        # Server config
        self.HOST_IP: str = os.getenv("HOST_IP", "127.0.0.1")
        self.HOST_PORT: int = int(os.getenv("HOST_PORT", 5000))
        self.RELOAD_API: bool = os.getenv("RELOAD_API", "False").lower() in (
            "true",
            "1",
        )

        # API config
        self.API_TITLE: str = "api.ajholzer.net"
        self.API_VERSION: str = "1.0.0"

    def check(self) -> None:
        """Checks the config for missing values.

        Raises:
            ValueError: When a value is not specified for a config key.
        """
        if not self.GITHUB_TOKEN:
            raise ValueError("'GITHUB_TOKEN' must be specified in the .env file!")

        if not self.GITHUB_USERNAME:
            raise ValueError("'GITHUB_USERNAME' must be specified in the .env file!")

        if not self.GITHUB_WEBSITE_SECRET:
            raise ValueError(
                "'GITHUB_WEBSITE_SECRET' must be specified in the .env file!"
            )


config = Config()
