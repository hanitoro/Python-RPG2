"""Локальная проверка комнат. Стандартная библиотека, без интернета.

Команды: python CHECK.py 1 / 2 / 3 / 4
После успешной проверки создаётся checks/stage_N.json.
Этот протокол нужно вместе с исправленным файлом загрузить в игровой чат.
"""

from __future__ import annotations
import ast
import contextlib
import importlib
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks"
CHECKS = ROOT / "checks"
FILENAMES = {1: "terminal.py", 2: "trader.py", 3: "vault.py", 4: "guardian.py"}


def fnv1a(data: bytes) -> str:
    h = 0x811C9DC5
    for b in data:
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def worker(stage: int) -> dict:
    sys.path.insert(0, str(TASKS))
    scores: list[dict] = []

    def test(label, fn):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = fn()
            if result is not True:
                raise AssertionError('результат не соответствует условию')
            scores.append({"name": label, "ok": True})
        except Exception as exc:
            scores.append({"name": label, "ok": False, "detail": f"{type(exc).__name__}: {exc}"})

    module_name = {1: "terminal", 2: "trader", 3: "vault", 4: "guardian"}[stage]
    with contextlib.redirect_stdout(io.StringIO()):
        m = importlib.import_module(module_name)

    if stage == 1:
        test('access_message возвращает нужную строку', lambda: m.access_message('Лира') == 'Доступ: Лира')
        test('boot формирует полный ответ для Лиры', lambda: m.boot('Лира') == 'ONLINE | Доступ: Лира')
        test('boot работает с другим именем', lambda: m.boot('Марк') == 'ONLINE | Доступ: Марк')

        def no_print():
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                m.boot('Тест')
            return stream.getvalue() == ''
        test('boot не выводит сообщения сам', no_print)

    elif stage == 2:
        test('цена со скидкой 10%', lambda: abs(m.total_cost(100, 2, 10) - 180) < 1e-9)
        test('без скидки', lambda: abs(m.total_cost(50, 1) - 50) < 1e-9)
        test('скидка 20%', lambda: abs(m.total_cost(5, 2, 20) - 8) < 1e-9)
        test('100% скидка', lambda: abs(m.total_cost(8, 3, 100) - 0) < 1e-9)
        def raises(*args):
            try:
                m.total_cost(*args)
            except ValueError:
                return True
            return False
        test('отрицательная цена вызывает ValueError', lambda: raises(-3, 2, 0))
        test('нулевое количество вызывает ValueError', lambda: raises(3, 0, 0))
        test('скидка 120% вызывает ValueError', lambda: raises(3, 2, 120))
        test('отрицательная скидка вызывает ValueError', lambda: raises(3, 2, -1))

    elif stage == 3:
        def independent():
            a = m.Adventurer('Рыцарь'); b = m.Adventurer('Алхимик')
            a.add_item('Меч')
            return a.list_items() == ['Меч'] and b.list_items() == []
        test('инвентари двух героев независимы', independent)
        test('у нового героя пустая сумка', lambda: m.Adventurer('Новый').list_items() == [])
        def remove_works():
            a = m.Adventurer('Рыцарь'); a.add_item('Ключ')
            return a.remove_item('Ключ') is True and a.list_items() == []
        test('удаление существующего предмета', remove_works)
        def remove_missing():
            a = m.Adventurer('Рыцарь')
            return a.remove_item('Нет такого') is False
        test('удаление отсутствующего предмета', remove_missing)
        def returned_copy():
            a = m.Adventurer('Рыцарь'); a.add_item('Свиток')
            copy = a.list_items(); copy.append('Подмена')
            return 'Подмена' not in a.list_items()
        test('list_items возвращает копию', returned_copy)

    elif stage == 4:
        good = lambda size: {"name": "record.txt", "checksum_ok": True, "size": size}
        bad = lambda size: {"name": "record.txt", "checksum_ok": False, "size": size}
        test('хороший файл разрешён', lambda: m.scan_file(good(42)) == 'ALLOW')
        test('маленький хороший файл разрешён', lambda: m.scan_file(good(1)) == 'ALLOW')
        test('нулевой размер блокируется', lambda: m.scan_file(good(0)) == 'BLOCK')
        test('отрицательный размер блокируется', lambda: m.scan_file(good(-3)) == 'BLOCK')
        test('неверная контрольная сумма блокируется', lambda: m.scan_file(bad(42)) == 'BLOCK')

        tests_path = TASKS / 'student_tests.py'
        def meaningful_asserts():
            tree = ast.parse(tests_path.read_text(encoding='utf-8'))
            calls = []
            expected = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Assert):
                    c = [n for n in ast.walk(node.test)
                         if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'scan_file']
                    if c:
                        calls.append(node)
                        for item in ast.walk(node.test):
                            if isinstance(item, ast.Constant) and item.value in ('ALLOW', 'BLOCK'):
                                expected.add(item.value)
            return len(calls) >= 2 and expected == {'ALLOW', 'BLOCK'}
        test('свои два assert с вызовом scan_file', meaningful_asserts)
        def custom_tests_run():
            mod = importlib.import_module('student_tests')
            mod.run_student_tests()
            return True
        test('пользовательские assert выполняются', custom_tests_run)

    return {"tests": scores, "passed": all(x['ok'] for x in scores)}


def run_stage(stage: int):
    CHECKS.mkdir(exist_ok=True)
    proof_path = CHECKS / f'stage_{stage}.json'
    proof_path.unlink(missing_ok=True)  # старый успешный протокол не использовать после новых правок
    try:
        run = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(stage)],
                             capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=12)
    except subprocess.TimeoutExpired:
        print('\n[!] Программа слишком долго работает. Проверь бесконечные циклы и input() вне if __name__ == "__main__".')
        return 1
    if run.returncode:
        print('\n[!] Не получилось запустить проверяемый модуль.')
        print((run.stderr or run.stdout)[-2200:])
        return 1
    try:
        report = json.loads(run.stdout)
    except json.JSONDecodeError:
        print('[!] Некорректный ответ проверки:', run.stdout[-800:]); return 1
    for i, item in enumerate(report['tests'], 1):
        print(f"{'[OK]' if item['ok'] else '[X] '} {i}. {item['name']}")
        if not item['ok']:
            print('     ', item.get('detail', 'проверь логику'))
    number = sum(x['ok'] for x in report['tests']); total = len(report['tests'])
    print(f'\nПроверено: {number}/{total}')
    if report['passed']:
        source = TASKS / FILENAMES[stage]
        proof = {"game": "AURION_GHOST_QUEST", "version": 1, "stage": stage,
                 "file_name": source.name, "file_hash": fnv1a(source.read_bytes()),
                 "checks_passed": number, "checks_total": total, "passed": True}
        if stage == 4:
            extra = TASKS / "student_tests.py"
            proof["extra_files"] = [{"file_name": extra.name, "file_hash": fnv1a(extra.read_bytes())}]
        proof_path.write_text(json.dumps(proof, ensure_ascii=False, indent=2), encoding='utf-8')
        print('\nУСПЕХ. Готов протокол:', proof_path.relative_to(ROOT))
        print('В мессенджере выбери отредактированный файл и этот JSON-протокол.')
        return 0
    print('\nПока не пройдено. Исправь ошибки в файле и запусти проверку ещё раз.')
    return 1


def main():
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print('Используй: python CHECK.py 1, 2, 3 или 4'); return 2
    if len(sys.argv) == 3 and sys.argv[1] == '--worker':
        try:
            stage = int(sys.argv[2]); print(json.dumps(worker(stage), ensure_ascii=False))
            return 0
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)
            import traceback; traceback.print_exc(file=sys.stderr)
            return 1
    try: stage = int(sys.argv[1]); assert stage in FILENAMES
    except Exception:
        print('Номер комнаты должен быть 1, 2, 3 или 4'); return 2
    return run_stage(stage)


if __name__ == '__main__':
    raise SystemExit(main())
