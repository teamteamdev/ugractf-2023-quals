from flask import Flask, make_response, render_template, request
import hmac
from werkzeug.middleware.proxy_fix import ProxyFix
from math import ceil

FLAG_1 = "flag_part1: ugra_triangles_are_cool_"
FLAG_2 = "flag_part2: but_triflags_are_"
FLAG_3 = "way_cooler_"
FLAG_SECRET = b"NDAwNmZiZDYtM2Y4MC00ZTJkLTg3MDct"
SUFFIX_SIZE = 12

def get_flag_suffix(token):
    return hmac.new(FLAG_SECRET, token.encode(), "sha256").hexdigest()[:SUFFIX_SIZE]

def make_app(state_dir):

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for = 1, x_host = 1)

    @app.route("/robots.txt")
    def robots():
        r = make_response("User-Agent: *\nDisallow: /secret-page/\n")
        r.status = 200
        r.mimetype = "text/plain"
        r.headers["Content-Type"] = "text/plain; charset=utf-8"
        return r
    
    @app.route("/secret-page/")
    def secret():
        return FLAG_2

    @app.route("/favicon.ico/")
    def icon():
        return "not found", 404
    
    @app.route("/<token>/")
    def index(token):
        resp = make_response(render_template("index.html", flag_1 = FLAG_1))
        if len(token) == 16:
            resp.headers['x-flag-part3'] = FLAG_3 + get_flag_suffix(token)
        return resp
    
    @app.route("/<token>/robots.txt")
    def token_robots(token):
        r = make_response("Allow: *\n# overrides root robots.txt\n")
        r.status = 200
        r.mimetype = "text/plain"
        r.headers["Content-Type"] = "text/plain; charset=utf-8"
        return r
    
    return app
