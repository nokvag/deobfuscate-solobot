import ast
import builtins
import re
import pathlib

# Читаем код из файла
code = pathlib.Path("layer5.py").read_text()
tree = ast.parse(code)

replacements = {}

# Ищем присваивания вида: a, b = str, int (все имена)
for node in tree.body:
    if isinstance(node, ast.Assign):
        target = node.targets[0]
        value = node.value

        if isinstance(target, ast.Tuple) and isinstance(value, ast.Tuple):
            if len(target.elts) == len(value.elts):
                for tgt, val in zip(target.elts, value.elts):
                    if (
                        isinstance(tgt, ast.Name)
                        and isinstance(val, ast.Name)
                        and val.id in dir(builtins)
                    ):
                        replacements[tgt.id] = val.id

# Подготовка паттерна и замена
if replacements:
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, replacements)) + r")\b")

    def rename(match):
        return replacements[match.group(0)]

    clean_code = pattern.sub(rename, code)
else:
    clean_code = code  # Ничего не заменяем

# Сохраняем результат
pathlib.Path("stage1.py").write_text(clean_code)
print(f"Заменено {len(replacements)} переменных. Результат сохранён в stage1.py")