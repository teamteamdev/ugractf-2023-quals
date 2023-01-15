import os
import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, render_template, redirect

from kyzylborda_lib.secrets import get_flag, get_secret, validate_token


class TokenError(ValueError):
    pass


class Weblog:
    def __init__(self, state_dir):
        self.state_dir = state_dir
        self.cursors = {}

    def get_cursor(self, token):
        if not validate_token(token):
            raise TokenError("Invalid token")
        if token not in self.cursors:
            con = sqlite3.connect(
                f"{self.state_dir}/dbs/{token}.db", isolation_level=None)
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, content TEXT)")
            self.cursors[token] = cur
            if not self.get_comments(token):
                self.post_comment(
                    token, "admin", "Что-то тихо тут. Меня кто-нибудь читает?")
                self.post_comment(token, "petya233", "читаем,  читаем")
                self.post_comment(
                    token, "testacc", "Вась, может расскажешь, как ты блог написал?")
                self.post_comment(
                    token, "admin", "Да там скучно, Flask и куча костылей. Зато теперь <b>форматирование</b> <i>работает</i>, а не как раньше.")
                self.post_comment(
                    token, "testacc", "Что, прям работает? <b><i><blink>тест тест тест</blink></i></b>")
                self.post_comment(
                    token, "h4srr", "ну-ка, а так? <style>spoiler { color: grey; background-color: grey; } spoiler:hover { color: inherit; background-color: inherit; }</style> <spoiler>тест</spoiler>")
                self.post_comment(
                    token, "h4srr", "да, и правда работает. это уже выглядит несколько опасно, но сойдет. в общем, теперь в комментариях работают спойлеры, пользоваться ими вот так: &lt;spoiler&gt;текст спойлера&lt;/spoiler&gt;")
                self.post_comment(
                    token, "admin", "О, а как ты это сделал?")
                self.post_comment(
                    token, "h4srr", "а это секрет)")
        return self.cursors[token]

    def get_comments(self, token):
        cur = self.get_cursor(token)
        return [
            {
                "id": row[0],
                "author": row[1],
                "content": row[2]
            }
            for row in cur.execute("SELECT id, author, content FROM comments ORDER BY id ASC").fetchall()
        ]

    def post_comment(self, token, author, content):
        cur = self.get_cursor(token)
        cur.execute(
            "INSERT INTO comments (author, content) VALUES (?, ?)", (author, content))

    def reset_db(self, token):
        if not validate_token(token):
            raise TokenError("Invalid token")
        try:
            os.unlink(f"{self.state_dir}/dbs/{token}.db")
        except FileNotFoundError:
            pass
        if token in self.cursors:
            del self.cursors[token]


def make_app(state_dir):
    weblog = Weblog(state_dir)

    app = Flask(__name__)
    # Required for server to correctly redirect.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    @app.errorhandler(404)
    def page_not_found(e):
        return f"Don't forget your token: {request.path}"

    @app.route("/<token>/post", methods=["POST"])
    def post(token):
        try:
            form = request.form
            weblog.post_comment(token, form["author"], form["content"])
            return redirect(f"/{token}/", code=302)
        except TokenError:
            return "Invalid token"

    @app.route("/<token>/__reset_db__", methods=["POST"])
    def reset_db(token):
        try:
            weblog.reset_db(token)
            return redirect(f"/{token}/", code=302)
        except TokenError:
            return "Invalid token"

    @app.route("/<token>/")
    def front_page(token):
        try:
            authorized_login = request.cookies.get(
                "session") == get_secret("admin", token)
            flag = get_flag(token)
            return render_template("index.html", comments=weblog.get_comments(token), authorized_login=authorized_login, flag=flag)
        except TokenError:
            return "Invalid token"

    return app
