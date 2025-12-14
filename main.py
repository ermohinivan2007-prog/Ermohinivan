import sys
import argparse
import re
from typing import Tuple, List, Any, Dict

Token = Tuple[str, str, int, int]

class LexerError(Exception):
    pass

class ParseError(Exception):
    pass

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.length = len(text)

    def _peek(self, n=0) -> str:
        if self.pos + n >= self.length:
            return ''
        return self.text[self.pos + n]

    def _advance(self, n=1):
        for _ in range(n):
            if self.pos >= self.length:
                return
            ch = self.text[self.pos]
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1

    def _match(self, s: str) -> bool:
        return self.text.startswith(s, self.pos)

    def _skip_whitespace_and_comments(self):
        while True:
            progressed = False
            while self._peek() and self._peek().isspace():
                self._advance()
                progressed = True
            if self._match("=begin"):
                self._advance(6)
                while not self._match("=cut"):
                    if self.pos >= self.length:
                        raise LexerError("Unterminated multiline comment")
                    self._advance()
                self._advance(4)
                progressed = True
                continue
            if not progressed:
                break

    def _read_while(self, cond):
        start = self.pos
        while self.pos < self.length and cond(self.text[self.pos]):
            self._advance()
        return self.text[start:self.pos]

    def tokens(self):
        tokens = []
        while True:
            self._skip_whitespace_and_comments()
            if self.pos >= self.length:
                break

            ch = self._peek()
            line, col = self.line, self.col

            if self._match("var"):
                tokens.append(("VAR", "var", line, col))
                self._advance(3)
                continue

            if re.match(r'[_a-zA-Z]', ch):
                ident = self._read_while(lambda c: re.match(r'[_a-zA-Z0-9]', c))
                tokens.append(("IDENT", ident, line, col))
                continue

            if self._match("@("):
                tokens.append(("ATLPAREN", "@(", line, col))
                self._advance(2)
                continue

            if self._match("$["):
                tokens.append(("DICT_START", "$[", line, col))
                self._advance(2)
                continue

            if ch in "]:,()":
                tokens.append((ch, ch, line, col))
                self._advance()
                continue

            if ch == '"':
                self._advance()
                s = ""
                while self._peek() != '"':
                    if self.pos >= self.length:
                        raise LexerError("Unterminated string")
                    s += self._peek()
                    self._advance()
                self._advance()
                tokens.append(("STRING", s, line, col))
                continue

            if ch.isdigit() or (ch == '.' and self._peek(1).isdigit()):
                m = re.match(r'\d*\.\d+', self.text[self.pos:])
                if not m:
                    raise LexerError("Invalid number")
                tokens.append(("NUMBER", m.group(0), line, col))
                self._advance(len(m.group(0)))
                continue

            raise LexerError(f"Unexpected character {ch}")

        tokens.append(("EOF", "", self.line, self.col))
        return tokens

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos]

    def _advance(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def parse(self):
        values = []
        while self._peek()[0] != "EOF":
            values.append(self._parse_value())
        return values

    def _parse_value(self):
        t = self._peek()
        if t[0] == "NUMBER":
            return float(self._advance()[1])
        if t[0] == "STRING":
            return self._advance()[1]
        if t[0] == "DICT_START":
            return self._parse_dict()
        raise ParseError("Invalid value")

    def _parse_dict(self):
        self._advance()
        d = {}
        while self._peek()[0] != "]":
            key = self._advance()[1]
            self._advance()
            val = self._parse_value()
            d[key] = val
            if self._peek()[0] == ",":
                self._advance()
        self._advance()
        return d

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", "-o", required=True)
    args = parser.parse_args()
    input_text = sys.stdin.read()

if __name__ == "__main__":
    main()

