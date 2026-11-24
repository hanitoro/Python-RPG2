"""Твои два собственных теста для Смотрителя.

Напиши минимум ДВА разных assert, которые вызывают scan_file(...)
и проверяют правильный результат. Примеры ниже — подсказки, но не готовые тесты.

Один тест должен проверять нормальный файл (ожидается ALLOW),
другой — повреждённый (ожидается BLOCK).
После исправления guardian.py запусти CHECK_4.bat.
"""

from guardian import scan_file


def run_student_tests():
    assert scan_file({"name": "notes.txt", "checksum_ok": True, "size": 42}) == "ALLOW"
    assert scan_file({"name": "broken.txt", "checksum_ok": False, "size": 42}) == "BLOCK"


if __name__ == "__main__":
    run_student_tests()
    print("Пользовательские проверки выполнены")
