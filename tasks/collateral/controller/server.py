from kyzylborda_lib.sandbox import start_box
from kyzylborda_lib.secrets import validate_token, get_flag
from kyzylborda_lib.server import http


def init(box):
    with box.open("/flag", "w") as f:
        f.write(get_flag(box.token))


@http.listen
async def handle(request: http.Request):
    token = request.path[1:].partition("/")[0]
    if not validate_token(token):
        return http.respond(404)
    return await start_box(token, init=init)
