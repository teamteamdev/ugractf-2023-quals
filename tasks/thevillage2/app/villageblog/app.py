import os

from kyzylborda_lib.secrets import validate_token, get_flag
from starlette.applications import Starlette
from starlette.datastructures import URL
from starlette.middleware import Middleware
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.types import Receive, Send, Scope

from villageblog import routes


class FlagMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        url = URL(scope=scope)

        try:
            token = url.path.split("/")[1]
        except:
            token = ""

        if not validate_token(token):
            return await PlainTextResponse("Not found", status_code=404)(scope, receive, send)
        
        scope["flag"] = get_flag(token)

        return await self.app(scope, receive, send)


if os.environ.get("DEBUG") == "yes":
    from kyzylborda_lib.secrets import get_token, get_flag
    debug_token = get_token("123")
    print("Use this token:", debug_token)
    print("Here is the flag for you:", get_flag(debug_token))


app = Starlette(
    debug=os.environ.get("DEBUG") == "yes",
    routes=[
        Route("/{token}/", routes.main, name="main"),
        Route("/{token}/subscribe.xhtml", routes.subscribe, name="subscribe"),
        Route("/{token}/post-{id:int}.xhtml", routes.post, name="post"),
        Route("/{token}/tr/{full_id}", routes.post_encoded, name="post-data"),
        Mount("/{token}/static/", StaticFiles(directory="villageblog/static"), name="static"),
    ],
    middleware=[Middleware(FlagMiddleware)]
)
