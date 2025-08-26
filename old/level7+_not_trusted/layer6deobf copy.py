import re, pathlib, ast, astor
RAW_KEY = (
    0o1464, 0o1565, 0o1575, 0o1602, 0o1615, 0o1631, 0o1640, 0o1551,
    0o1533, 0o1547, 0o1655, 0o1653, 0o1567, 0o1666, 0o0155, 0o1605,
    0o1632, 0o1565, 0o1704, 0o1710, 0o1720, 0o1730, 0o1543, 0o1553,
    0o1563, 0o1574, 0o1525, 0o1540, 0o1555, 0o1565, 0o1575, 0o1604,
    0o1614, 0o1624, 0o1633, 0o1643, 0o1653, 0o1663, 0o1673, 0o1703,
)


KEY = bytes(v & 0xFF for v in RAW_KEY)        # как было

def deob(data: bytes) -> bytes:               # как было
    return bytes(b ^ KEY[i % 40] for i, b in enumerate(data))

code = pathlib.Path("layer6.py").read_text()

# ► новый паттерн: захватываем _целую_ байтовую строку (с кавычками)
pattern = re.compile(
    r"u1KQ2EguJKQ7\(\s*(b[ruRU]?[\'\"][^\"]*[\'\"])s*\)",   # DOTALL если нужны переносы
    re.DOTALL,
)

def repl(match: re.Match):
    byte_literal = match.group(1)         # например  b"G\x07\x88\xfeME"
    blob = ast.literal_eval(byte_literal) # превращаем в объект bytes
    return repr(deob(blob))               # → b"..."

new_code, n = pattern.subn(repl, code)
print(f"Замен: {n}")

pathlib.Path("stage2.py").write_text(new_code)
print("√ слой 6 снят → stage2.py")