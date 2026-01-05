# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import importlib
import pkgutil
import uvicorn

from fastapi import FastAPI, APIRouter
from typing import Optional
from config import config


class API:
    def __init__(self) -> None:
        """Initializes the API and registers all routes at _api/routes_."""
        # Init FastAPI
        self.__api: FastAPI = FastAPI(
            title=config.API_TITLE,
            version=config.API_VERSION,
        )

        # Register routes
        self.__register_routes()

    def __register_routes(self) -> None:
        """Registers all routes in _api/routes/_"""
        import api.routes

        for module_info in pkgutil.iter_modules(api.routes.__path__):
            # Skip private modules
            if module_info.name.startswith("_"):
                continue

            # Import module from api/routes
            module = importlib.import_module(f"api.routes.{module_info.name}")

            # Get router from module
            router: Optional[APIRouter] = getattr(module, "router", None)

            # Skip if router is not specified
            if router is None:
                continue

            # Get prefix and tags
            prefix: str = getattr(module, "PREFIX", "")
            tags: list[str] = getattr(module, "TAGS", [])

            # Add route to router
            self.__api.include_router(router=router, prefix=prefix, tags=tags)  # type: ignore

            # Log debug information
            print(f"✅ Registered route: {prefix or '/'}")

    def start(self) -> None:
        """Starts the API."""
        # Log debug information
        print(
            f"🟠 Starting API: ip='{config.HOST_IP}', port={config.HOST_PORT}, auto-reload: {config.RELOAD_API}"
        )

        # Start api
        uvicorn.run(
            app=self.__api,
            host=config.HOST_IP,
            port=config.HOST_PORT,
            reload=config.RELOAD_API,
        )
