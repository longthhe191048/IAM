# Understanding Obfuscate
## What is obfuscation? why do we need it?
* Obfuscation can simply mean making a piece of code unclear or difficult to understand.
* Obfuscation hides function and class names in your compiled Dart code, replacing each symbol with another symbol, making it difficult for an attacker to reverse engineer your proprietary app
* Encrypting some or all of a program's code is one obfuscation method
* Other approaches include stripping out potentially revealing metadata, replacing class and variable names with meaningless labels, and adding unused or meaningless code to an application script.

<img width="384" height="131" alt="image" src="https://github.com/user-attachments/assets/b5c421d8-38ba-49ba-9607-b1863f69542f" />

## Type of obfuscation
* Code Minification
* Code Randomization
* String Obfuscation
* Code Encryption

## obfuscate a code
**Original code**
```
print("Hello world!")
```
Applied string obfuscation
```
# string_obf_make.py
import base64, sys
XOR_KEY = 0x5A
ADD = 7
NOISE = "n0"

def make_payload(s):
    b = s.encode('utf-8')
    trans = bytes(((c ^ XOR_KEY) + ADD) & 0xFF for c in b)
    hex_pairs = "".join(f"{x:02x}" for x in trans)
    interleaved = "".join(hex_pairs[i:i+2] + NOISE for i in range(0, len(hex_pairs), 2))
    return base64.b64encode(interleaved.encode('ascii')).decode('ascii')

if __name__ == "__main__":
    plain = sys.argv[1]
    print(make_payload(plain))

```
Applied minification
```
# minify.py
import sys
src = open(sys.argv[1], 'r', encoding='utf-8').read()
out_lines = []
in_multiline_string = False
for line in src.splitlines():
    s = line.rstrip()
    # naive detection of multiline string start/end (""" or ''')
    if s.count('"""') % 2 == 1 or s.count("'''") % 2 == 1:
        in_multiline_string = not in_multiline_string
    if in_multiline_string:
        out_lines.append(s)
        continue
    # drop full-line comments and blank lines
    if s.strip().startswith("#") or s.strip() == "":
        continue
    # collapse multiple spaces; keep indentation minimal
    out_lines.append(s)
# very simple: join with newline (keeps readability but removes blanks)
print("\n".join(out_lines))
```
Applied Randomizer
```
# randomize_simple.py
import ast, astor, random, sys, keyword, builtins

IDENT_CHARS = "abcdefghijklmnopqrstuvwxyz"
def make_ident(rng, length=6):
    return ''.join(rng.choice(IDENT_CHARS) for _ in range(length))

class SimpleRenamer(ast.NodeTransformer):
    def __init__(self, rng):
        self.rng = rng
        self.map = {}
        self.reserved = set(keyword.kwlist) | set(dir(builtins))

    def _new(self, name):
        if name in self.map:
            return self.map[name]
        if name in self.reserved: return name
        new = make_ident(self.rng, 7)
        # avoid collisions
        while new in self.map.values():
            new = make_ident(self.rng, 7)
        self.map[name] = new
        return new

    def visit_FunctionDef(self, node):
        node.name = self._new(node.name)
        # rename args
        for a in node.args.args:
            a.arg = self._new(a.arg)
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load, ast.Del)):
            if node.id in self.map:
                node.id = self.map[node.id]
            else:
                # only rename non-reserved short names heuristically
                if not node.id.startswith("__") and node.id not in self.reserved and node.id.isidentifier():
                    node.id = self._new(node.id)
        return node

if __name__ == "__main__":
    seed = 42
    rng = random.Random(seed)
    src = open(sys.argv[1], "r", encoding="utf-8").read()
    tree = ast.parse(src)
    ren = SimpleRenamer(rng)
    tree = ren.visit(tree)
    ast.fix_missing_locations(tree)
    print(astor.to_source(tree))

```
Applied Code encryption

```
# encrypt_code_aes.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64, sys

# 16-byte AES key for demo (in practice, keep secret)
KEY = get_random_bytes(16)

def pad(s):
    pad_len = 16 - (len(s) % 16)
    return s + bytes([pad_len])*pad_len

if __name__ == "__main__":
    src = open(sys.argv[1],"rb").read()
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(src))
    print("KEY_HEX:", KEY.hex())
    print("IV_HEX:", iv.hex())
    print("BLOB:", base64.b64encode(ct).decode('ascii'))
```
Aplied mix
```
import base64;_k=0x77;def AUaZtxmr(s):b=base64.b64decode(s);return bytes((c^0x77) for c in b);KBkxhBqJ='HhoHGAUDVxUWBBJBQ0woL0pOR0woNkpATCg5SlAZRwRQfRMSEVcoKBNfB15NfVceShUWBBJBQ1kVQUMTEhQYExJfB15ZExIUGBMSX1AWBBQeHlBeTARKLCpMNCpZVQk0WwQjAhYKCg1ZUVwPDhkaGV5eQ0pQhQGChpZQh0qR01DVBeXg==';OlNJlwVU=AUaZtxmr(KBkxhBqJ);exec(OlNJlwVU.decode())
```
## Reference
* [How Obfuscation Works in Software Development](https://medium.com/@hendurhance/how-obfuscation-works-in-software-development-7f52edfff520)
* [What is obfuscation and how does it work?](https://www.techtarget.com/searchsecurity/definition/obfuscation)
* [Obfuscate Dart code](https://docs.flutter.dev/deployment/obfuscate)
