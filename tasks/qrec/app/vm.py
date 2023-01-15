import sys
import time
from collections import deque


class Registers(dict):

    def __init__(self, registers):
        self.registers = registers
        super().__init__()
        for letter in registers:
            self[letter] = 0

    def __missing__(self, key):
        return int(key)

    def __contains__(self, key):
        return key in self.registers


class VM:
    MAX_STACK_SIZE = 1000
    MAX_VALUE = 2**31
    MAX_CODE_SIZE = 2048
    VALID_NUMBERS = set(str(n) for n in range(-10, 11))

    def __init__(self, code):
        self.error = ''
        self.reset_state()
        self._compile(code)

    def reset_state(self):
        self.stack = []
        self.registers = Registers('abcd')

    def is_state_valid(self):
        if len(self.stack) > VM.MAX_STACK_SIZE:
            self.error = 'stack overflow'
            return False
        if any(abs(v) > VM.MAX_VALUE for v in self.registers.values()):
            self.error = 'value overflow'
            return False
        return True

    def run(self, timeout=1):
        if self.error:
            return
        pos = 0
        start = time.monotonic()
        while self.is_state_valid() and pos < len(self.code):
            cmd, a, b = self.code[pos]
            if cmd == 'push':
                self.stack.append(self.registers[a])
            elif cmd == 'pop':
                if not self.stack:
                    self.error = 'pop from empty stack'
                    return
                self.registers[a] = self.stack.pop()
            elif cmd == 'add':
                self.registers[a] += self.registers[b]
            elif cmd == 'sub':
                self.registers[a] -= self.registers[b]
            elif cmd == 'mul':
                self.registers[a] *= self.registers[b]
            elif cmd == 'div':
                if not self.registers[b]:
                    self.error = 'division by zero'
                    return
                self.registers[a] //= self.registers[b]
            elif cmd == 'mov':
                self.registers[a] = self.registers[b]
            elif cmd == 'jmp':
                pos = self._labels[a] - 1
            elif cmd == 'je':
                if self.registers[a] == 0:
                    pos = self._labels[b] - 1
            elif cmd == 'jl':
                if self.registers[a] < 0:
                    pos = self._labels[b] - 1
            elif cmd == 'jg':
                if self.registers[a] > 0:
                    pos = self._labels[b] - 1
            if timeout and time.monotonic() - start > timeout:
                self.error = 'timeout exceeded'
                return
            pos += 1

    def _compile(self, code):

        def check(arg):
            return arg in self.registers or arg in VM.VALID_NUMBERS

        self._labels = {}
        lines = deque(line.strip() for line in code.splitlines())
        self.code = []
        defines = {}
        defines_count = {}
        used_labels = set()
        while lines:
            if len(self.code) > VM.MAX_CODE_SIZE:
                self.error = 'generated code is too big'
                return
            line = lines.popleft().lower()
            if not line or line.startswith('//'):
                continue
            if line.endswith('!'):
                name = line[:-1]
                content = defines.get(name)
                if not content:
                    self.error = 'call of not defined macro'
                    return
                label_prefix = f'{name}-{defines_count[name]}#'
                for l in content:
                    if l.endswith(':'):
                        l = label_prefix + l
                    elif '{}' in l:
                        if l.count('{}') > 1:
                            self.error = 'invalid label'
                            return
                        l = l.format(label_prefix)
                    lines.appendleft(l)
                defines_count[name] += 1
            elif line.startswith('#define'):
                line = line.split()
                if len(line) != 2:
                    self.error = 'invalid define syntax'
                    return
                _, name = line
                if name in defines:
                    self.error = 'redefine a macro'
                    return
                content = []
                bad_line = f'{name}!'
                while lines:
                    n = lines.popleft()
                    if n == '#enddefine':
                        break
                    elif n == bad_line:
                        self.error = 'not able to call macro in thisself'
                        return
                    content.append(n)
                defines[name] = list(reversed(content))
                defines_count[name] = 0
            elif line == '#enddefine':
                self.error = 'enddefine without define'
                return
            elif line.endswith(':'):
                label = line[:-1]
                if len(label.split()) != 1:
                    self.error = 'invalid label name format'
                    return
                if label in self._labels:
                    self.error = 'redeclare label'
                    return
                self._labels[label] = len(self.code)
            else:
                cmd, *args = line.split()
                if cmd == 'push' and len(args) == 1:
                    arg = args[0]
                    if not check(arg):
                        self.error = 'invalid arg in push'
                        return
                    self.code.append(('push', arg, None))
                elif cmd == 'pop' and len(args) == 1:
                    arg = args[0]
                    if arg not in self.registers:
                        self.error = 'invalid arg in pop'
                        return
                    self.code.append(('pop', arg, None))
                elif cmd == 'add' and len(args) == 2:
                    if args[0] not in self.registers or not check(args[1]):
                        self.error = 'invalid arg in add'
                        return
                    a, b = args
                    self.code.append(('add', a, b))
                elif cmd == 'sub' and len(args) == 2:
                    if args[0] not in self.registers or not check(args[1]):
                        self.error = 'invalid arg in sub'
                        return
                    a, b = args
                    self.code.append(('sub', a, b))
                elif cmd == 'mul' and len(args) == 2:
                    if args[0] not in self.registers or not check(args[1]):
                        self.error = 'invalid arg in mul'
                        return
                    a, b = args
                    self.code.append(('mul', a, b))
                elif cmd == 'div' and len(args) == 2:
                    if args[0] not in self.registers or not check(args[1]):
                        self.error = 'invalid arg in div'
                        return
                    a, b = args
                    self.code.append(('div', a, b))
                elif cmd == 'mov' and len(args) == 2:
                    if args[0] not in self.registers or not check(args[1]):
                        self.error = 'invalid arg in mov'
                        return
                    a, b = args
                    self.code.append(('mov', a, b))
                elif cmd == 'jmp' and len(args) == 1:
                    label = args[0]
                    if not (label[0] == label[-1] == '"'):
                        self.error = 'invalid label'
                        return
                    label = label[1:-1]
                    used_labels.add(label)
                    self.code.append(('jmp', label, None))
                elif cmd == 'je' and len(args) == 2:
                    arg, label = args
                    if not (label[0] == label[-1] == '"'):
                        self.error = 'invalid label'
                        return
                    label = label[1:-1]
                    if not check(arg):
                        self.error = 'invalid arg in je'
                        return
                    used_labels.add(label)
                    self.code.append(('je', arg, label))
                elif cmd == 'jl' and len(args) == 2:
                    arg, label = args
                    if not (label[0] == label[-1] == '"'):
                        self.error = 'invalid label'
                        return
                    label = label[1:-1]
                    if not check(arg):
                        self.error = 'invalid arg in jl'
                        return
                    used_labels.add(label)
                    self.code.append(('jl', arg, label))
                elif cmd == 'jg' and len(args) == 2:
                    arg, label = args
                    if not (label[0] == label[-1] == '"'):
                        self.error = 'invalid label'
                        return
                    label = label[1:-1]
                    if not check(arg):
                        self.error = 'invalid arg in jg'
                        return
                    used_labels.add(label)
                    self.code.append(('jg', arg, label))
                else:
                    print(f'undefined command: {cmd}', file=sys.stderr)
                    self.error = 'undefined command'
                    return
        for label in used_labels:
            if not label in self._labels:
                self.error = 'undefined label'
                return


if __name__ == '__main__':
    code = sys.stdin.read()
    vm = VM(code)
    if vm.error:
        print(f'Error while compiling code: {vm.error}', file=sys.stderr)
        sys.exit(1)
    vm.stack = [int(arg) for arg in sys.argv[1:]]
    vm.run(0)
    if vm.error:
        print(f'Error while executing: {vm.error}', file=sys.stderr)
        sys.exit(2)
    n = len(vm.stack)
    for i, v in enumerate(vm.stack):
        print(v, f'({n - i})')
