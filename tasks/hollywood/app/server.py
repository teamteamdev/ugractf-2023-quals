import asyncio
from werkzeug.middleware.proxy_fix import ProxyFix
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from quart import Quart, request, send_from_directory, websocket
import os.path

from kyzylborda_lib.secrets import get_flag


TIME_ACCURACY = 0.5


def make_app():
    app = Quart(__name__ )
    # Required for server to correctly redirect.
    app.asgi_app = ProxyHeadersMiddleware(app.asgi_app)

    @app.errorhandler(404)
    async def page_not_found(e):
        return f"Don't forget your token: {request.path}"

    @app.websocket("/<token>/ws")
    async def ws(token: str):
        flag = get_flag(token)

        await websocket.send("""
            await sleep(500);
            await type(`\n\nCONNECTED`);
            await sleep(1000);
            await type(`\n\nAUTHENTICATION REQUIRED`);
            await sleep(1000);
            render("");
            await type(`ENTER FLAG: `);
            ws.send(await input());
        """)

        while True:
            data = await websocket.receive()
            if not isinstance(data, str):
                pass

            prefix_len = len(os.path.commonprefix([flag, data]))

            time_seconds = (prefix_len + 1) ** 0.5
            await websocket.send("""
                await type(`\n\n`);
            """);
            for i in range(int(time_seconds / TIME_ACCURACY)):
                await asyncio.sleep(TIME_ACCURACY)
                percentage = round(i * TIME_ACCURACY / time_seconds * 100)
                await websocket.send(f"""
                    changeLine(`VERIFYING {'#' * (percentage // 2) + ' ' * (50 - percentage // 2)} {percentage}%`);
                """)
            await asyncio.sleep(time_seconds % TIME_ACCURACY)
            await websocket.send(f"""
                changeLine(`VERIFYING {'#' * 50} 100%`);
            """)

            if flag == data:
                await websocket.send("""
                    await sleep(1000);
                    render("");
                    await sleep(1000);
                    await type(`GREETINGS PROFESSOR FALKEN`);
                    await sleep(1000);
                    await type(`\n\nSHALL WE PLAY A GAME?`);
                """)
            else:
                await websocket.send("""
                    await type(`\n\nWRONG FLAG`);
                    await sleep(1000);
                    render("");
                    await type(`ENTER FLAG: `);
                    ws.send(await input());
                """)

    @app.route("/<token>/")
    async def index(token: str):
        return await send_from_directory("static", "index.html")

    return app
