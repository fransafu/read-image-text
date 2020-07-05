import os
import sys

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers


def run() -> None:
    web.run_app(
        register_graphql_handlers(
            app=web.Application(),
            engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/sdl",
            engine_modules=[
                "query_resolvers",
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True,
        )
    )

if __name__ == "__main__":
    sys.exit(run())