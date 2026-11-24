"""Комната 4. Последняя защита.

scan_file(record) получает СЛОВАРЬ:
{ "name": "notes.txt", "checksum_ok": True, "size": 42 }

Верни:
- "BLOCK", если контрольная сумма НЕ в порядке ИЛИ размер <= 0;
- "ALLOW", если контрольная сумма в порядке И размер > 0.

Это ИМИТАЦИЯ проверки, никаких реальных файлов мы не удаляем.
Не переименовывай функцию. После исправления допиши 2 assert в student_tests.py.
"""


def scan_file(record):
    if not record["checksum_ok"]:
        return "BLOCK"

    if record["size"] <= 0:
        return "BLOCK"

    return "ALLOW"


if __name__ == "__main__":
    print(scan_file({"name": "notes.txt", "checksum_ok": True, "size": 42}))
