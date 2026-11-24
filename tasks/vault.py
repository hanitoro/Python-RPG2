"""Комната 3. Проклятые артефакты.

Создавай независимые экземпляры Adventurer:
- Adventurer(name) хранит имя героя;
- add_item(item) добавляет предмет ТОЛЬКО этому герою;
- remove_item(item) возвращает True, если предмет удалён, иначе False;
- list_items() возвращает список предметов этого героя.

Проблема: инвентари двух героев mysteriously связаны.
Исправь хранение состояния, не изменяя названия методов.
"""


class Adventurer:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def list_items(self):
        return list(self.items)


if __name__ == "__main__":
    knight = Adventurer("Рыцарь")
    mage = Adventurer("Алхимик")
    knight.add_item("Меч")
    print("Рыцарь:", knight.list_items())
    print("Алхимик:", mage.list_items())  # Здесь должно быть пусто.
