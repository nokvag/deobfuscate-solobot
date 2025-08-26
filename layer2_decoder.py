# auto_deobf.py
import re, base64

with open('layer1.py', encoding='utf-8') as f:
    src = f.read()

m = re.search(r"b'([^']+)'", src, re.DOTALL)
if not m:
    raise RuntimeError("Не найден b85-блок")
data = m.group(1).encode('utf-8')
decoded = base64.b85decode(data)

# Печатаем распакованный текст
print(decoded.decode('utf-8', 'ignore'))