from kyzylborda_lib.secrets import get_flag
from functools import lru_cache
from random import choices
import gzip
import base64

from flask import Flask, render_template, request

from vm import VM

VM.MAX_VALUE = 200_000_000_000


def log_solution(code):
    compressed = gzip.compress(code.encode())
    encoded = base64.b64encode(compressed)
    print('Solution: ', encoded.decode(), flush=True)


def run(vm, x, fx):
    vm.reset_state()
    vm.stack = [x]
    vm.run()
    if vm.error:
        return False
    if vm.stack == [fx]:
        return True
    return False


@lru_cache(maxsize=None)
def f(n):
    if n == 1:
        return 1
    s = 0
    for i in range(1, n):
        if n % i == 0:
            s += f(i)
    s += n
    return s


TESTS = [(x, f(x)) for x in range(1, 512)]
MAX_CODE_SIZE = 1 * 1024
TESTS_PER_RUN = 64
STATIC_TESTS = 10


def test(vm):
    tests = TESTS[:STATIC_TESTS] + choices(TESTS[STATIC_TESTS:],
                                           k=TESTS_PER_RUN - STATIC_TESTS)
    return all(run(vm, x, fx) for x, fx in tests)


def make_app():
    app = Flask(__name__)

    @app.route('/specs/')
    def specs():
        return render_template('specs.html')

    @app.route('/<token>/', methods=['GET', 'POST'])
    def index(token):
        if request.method == 'GET':
            return render_template('index.html')
        form = request.form
        code = form.get('code')
        if not code:
            return 'No code sent'
        if len(code) > MAX_CODE_SIZE:
            return 'Max code size is 1kb'
        vm = VM(code)
        if vm.error:
            return f'Error while code compilation: {vm.error}'
        if test(vm):
            log_solution(code)
            return f'Good! And you flag is {get_flag(token)}'
        elif vm.error:
            return f'Oops, your code is not working, error is "{vm.error}"'
        else:
            return f'Oops, your code is not working, invalid answers'

    return app
