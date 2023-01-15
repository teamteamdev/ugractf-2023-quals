from __future__ import annotations

from collections import defaultdict
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, abort
import random

from kyzylborda_lib.secrets import get_flag, get_secret, validate_token


NESTING_LEVEL = 500


messages = []
for name in ["sudo-insults.txt", "quips.txt"]:
    with open(name) as f:
        messages += [line.strip() for line in f.readlines()]
messages = [message for message in messages if message]


def get_directory_content(state: str) -> dict[str, str | None]:
    children = {}
    j = -1
    for i in range(4):
        if i == 0:
            next_ref = get_secret("state", f"next:{state}")
        else:
            next_ref = None
        name = None
        while not name or name in children:
            j += 1
            name = get_secret("layer", f"{state}:{j}")
        children[name] = next_ref
    return children


def make_app(state_dir: str):
    app = Flask(__name__ )
    # Required for server to correctly redirect.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    @app.route("/<token>/")
    @app.route("/<token>/<path:path>")
    def serve(token: str, path: str=""):
        if not validate_token(token):
            abort(404)

        parts = [part for part in path.split("/") if part]
        state = get_secret("state", f"token:{token}")

        for part in parts:
            children = get_directory_content(state)
            if part in children:
                next_state = children[part]
                if next_state is None:
                    return random.Random(f"{state}:{part}").choice(messages)
                state = next_state
            else:
                abort(404)

        if len(parts) >= NESTING_LEVEL:
            return get_flag(token)

        html = f"<H1>Index of /{token}/{path}</H1>"
        if path != "":
            html += f"<A HREF=..>Parent Directory</A><BR>"

        children = get_directory_content(state)
        for file_name in sorted(children.keys()):
            html += f"<A HREF={file_name}/>{file_name}</A><BR>"

        return html


    return app
