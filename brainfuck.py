#!/usr/local/bin/python3
__author__ = 'Kellan Childers'


def brackets(function):
    def bracket_check(self, code, data):
        count = 0
        for i in code:
            if count < 0:
                break
            if i == '[':
                count += 1
            elif i == ']':
                count -= 1

        if count != 0:
            raise SyntaxError("Brackets not matched")

        return function(self, code, data)

    return bracket_check


def inputs(function):
    def input_check(self, code, data):
        needed = sum([1 for x in code if x == ','])

        if needed > len(data):
            raise SyntaxError("Not enough inputs for code")

        return function(self, code, data)

    return input_check


class Interpreter:
    @inputs
    @brackets
    def __init__(self, code, data):
        self.commands = {'+': self.add,
                         '-': self.sub,
                         '>': self.rmov,
                         '<': self.lmov,
                         ',': self.get,
                         '.': self.put,
                         '[': self.rep,
                         ']': self.rrep
                         }
        self.code = list(filter(
            lambda x: x in '+-><,.[]', code))
        self.input = list(data)
        self.output = ''
        self.memory = [0]
        self.ptr = 0
        self.sptr = 0

    def interpret(self):
        while self.sptr < len(self.code):
            self.execute()
        return self.output

    def execute(self):
        self.commands[self.code[self.sptr]]()
        # Debugging information.
        # print(self.code[self.sptr], self.ptr, self.memory, self.output)
        self.sptr += 1

    def add(self):
        if self.memory[self.ptr] != 255:
            self.memory[self.ptr] += 1
        else:
            self.memory[self.ptr] = 0

    def sub(self):
        if self.memory[self.ptr] != 0:
            self.memory[self.ptr] -= 1
        else:
            self.memory[self.ptr] = 255

    def rmov(self):
        self.ptr += 1
        while len(self.memory) <= self.ptr:
            self.memory.append(0)

    def lmov(self):
        self.ptr -= 1
        while len(self.memory) <= self.ptr:
            self.memory.append(0)

    def get(self):
        self.memory[self.ptr] = ord(self.input[0])
        del self.input[0]

    def put(self):
        self.output += chr(self.memory[self.ptr])

    def rep(self):
        if not self.memory[self.ptr]:
            # Skip the internals and go to the matching bracket.
            count, end = 0, 0
            for i, command in enumerate(self.code):
                if i <= self.sptr:
                    continue
                if command == '[':
                    count += 1
                elif command == ']':
                    if count == 0:
                        end = i
                        break
                    else:
                        count -= 1
            self.sptr = end

    def rrep(self):
        if self.memory[self.ptr]:
            # Repeat the internals by returning to matching bracket.
            count, beginning = 0, 0
            for i, command in enumerate(reversed(self.code)):
                if i < len(self.code) - self.sptr:
                    continue
                if command == ']':
                    count += 1
                elif command == '[':
                    count -= 1
                    if count < 0:
                        beginning = i
                        break
            self.sptr = len(self.code) - beginning - 1


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 2:
        _, code, data = argv
    elif len(argv) > 1:
        _, code = argv
        data = ''
    else:
        print("Correct Usage: arg[1] code, arg[2] input (optional)")
        print("Showing default hello world")
        code, data = ',[.[-],]', 'Hello World!' + chr(0)
        # ',>,[>+<-]<.', 'ab' is also an easy test.

    try:
        print(Interpreter(code, data).interpret())
    except SyntaxError as e:
        print(e.msg)
