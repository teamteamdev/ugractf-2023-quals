from collections import defaultdict
import ctypes
import json
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, send_from_directory
import os
import time
import traceback

from kyzylborda_lib.secrets import get_flag, validate_token


libmaze = ctypes.CDLL("./libmaze.so")


TIME_LIMIT = 10 * 60
N_LEVELS = 31


def generate_level(level: int, token: str):
    if level == 1:
        return {
            "field": generate_maze(7, 7, False, 5, 0),
            "text": "Hey there! <span style='color: #0f0'>@</span> is you. <span class='blink'>⚑</span> is flag. Go grab 'em."
        }
    elif level == 2:
        return {
            "field": generate_maze(7, 7, True, 5, 0),
            "text": "Of course it wouldn't be <i>that</i> easy!"
        }
    elif level == 3:
        return {
            "field": generate_maze(7, 7, True, 5, 1),
            "text": "<span style='color: #0ff'>■</span> is a portal."
        }
    elif level == 4:
        return {
            "field": generate_maze(7, 7, True, 5, 3),
            "text": "Differently colored portals connect different pairs of locations."
        }
    elif level == 5:
        return {
            "field": generate_maze(100, 100, True, 400, 10),
            "text": "Let's try bigger!"
        }
    elif level <= N_LEVELS - 1:
        return {
            "field": generate_maze(100, 100, True, 400, 10),
            "text": "Just one more level..."
        }
    elif level == N_LEVELS:
        return {
            "field": generate_maze(5, 5, False, 0, 0),
            "text": f"Take this treasure as a reward for your bravery! {get_flag(token)}"
        }


def generate_maze(height: int, width: int, add_maze: bool, points: int, portals: int) -> list[list[str]]:
    rows = 2 * height + 1
    cols = 2 * width + 1
    field = ctypes.create_string_buffer(rows * cols)
    if libmaze.generate_maze(field, height, width, add_maze, points, portals) == 0:
        raise ValueError("Maze generation failed")
    return [list(field.raw[i:i + rows].decode()) for i in range(0, rows * cols, rows)]


def make_level(level: int, token: str):
    result = generate_level(level, token)
    field = result["field"]
    portals = defaultdict(list)
    for y, line in enumerate(field):
        for x, c in enumerate(line):
            if c == "@":
                yc, xc = y, x
            elif "A" <= c <= "Z":
                portals[c].append([y, x])
    field[yc][xc] = " "
    return {
        "field": field,
        "portals": dict(portals),
        "text": result["text"],
        "cursor": [yc, xc]
    }


def load_session(state_dir: str, token: str):
    try:
        with open(os.path.join(state_dir, f"{token}.json")) as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "level": 1,
            "notice": "",
            "end_time": time.time() + TIME_LIMIT,
            **make_level(1, token)
        }
    except IOError:
        traceback.print_exc()
        return {
            "level": 1,
            "notice": "Something went wrong. Please notify administrators.",
            "end_time": time.time() + TIME_LIMIT,
            **make_level(1, token)
        }


def save_session(state_dir: str, token: str, session):
    path = os.path.join(state_dir, f"{token}.json")
    with open(f"{path}.tmp", "w") as f:
        json.dump(session, f)
    os.rename(f"{path}.tmp", path)


def session_iterate(session, key: str, token: str):
    if key == "R":
        session["level"] = 1
        session["notice"] = "You reset the game."
        session["end_time"] = time.time() + TIME_LIMIT
        session |= make_level(1, token)
        return

    if session["end_time"] is not None and time.time() > session["end_time"]:
        session["notice"] = "Timeout!"
        session["end_time"] = None
        return

    if key in "<>^vWASD":
        dy, dx = {
            "<": (0, -1),
            "A": (0, -1),
            ">": (0, 1),
            "D": (0, 1),
            "^": (-1, 0),
            "W": (-1, 0),
            "v": (1, 0),
            "S": (1, 0)
        }[key]
        yc, xc = session["cursor"]
        yc += dy
        xc += dx
        ch = session["field"][yc][xc]
        if ch == "#":
            session["notice"] = "You cannot go here!"
        elif ch == ".":
            session["notice"] = "You grabbed a flag!"
            session["field"][yc][xc] = " "
            if all("." not in line for line in session["field"]):
                session["level"] += 1
                session["notice"] = "Good job, you passed the level!"
                session |= make_level(session["level"], token)
                if session["level"] == N_LEVELS:
                    session["end_time"] = None
            else:
                session["cursor"] = [yc, xc]
        elif "A" <= ch <= "Z":
            session["notice"] = "You are standing on a portal. Press z to jump."
            session["cursor"] = [yc, xc]
        else:
            session["notice"] = ""
            session["cursor"] = [yc, xc]
    elif key == "Z":
        yc, xc = session["cursor"]
        ch = session["field"][yc][xc]
        if "A" <= ch <= "Z":
            coords = session["portals"][ch]
            yc, xc = coords[1] if coords[0] == [yc, xc] else coords[0]
            session["cursor"] = [yc, xc]
        else:
            session["notice"] = "You are not standing on a portal."


def make_app(state_dir: str):
    app = Flask(__name__ )
    # Required for server to correctly redirect.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    @app.errorhandler(404)
    def page_not_found(e):
        return f"Don't forget your token: {request.path}"

    @app.route("/<token>/api", methods=["POST"])
    def api(token: str):
        if not validate_token(token):
            return json.dumps({
                "level": 1,
                "notice": "Invalid token",
                "end_time": None,
                "field": [[" "]],
                "portals": {},
                "text": "",
                "cursor": [0, 0]
            })
        session = load_session(state_dir, token)
        keys = request.get_data()
        for key in keys:
            session_iterate(session, chr(key), token)
        save_session(state_dir, token, session)
        return json.dumps(session)

    @app.route("/<token>/")
    def hello(token: str):
        return send_from_directory("www", "index.html")

    return app
