import sys

from models import Student, ExcellentStudent
from operations import (
    students_with_grade_above,
    full_names,
    sort_by_grade,
    average_grade,
    average_grade_of_group,
    has_excellent_student,
    all_older_than,
    grades_list,
    group_to_count,
    unique_groups,
    process,
)
from generators import students_by_group, grade_squares, StudentIterator


# ---------- Демо-данные ----------

def build_demo_students() -> list:
    return [
        Student("Азаров Кирилл Дмитриевич", "ИСТ-24", 20, 3.9),
        Student("Малюков Дмитрий Георгиевич", "ИИ-24", 19, 3.8),
        Student("Сидорова Анна Петровна", "ИИ-25", 18, 3.9),
        Student("Кузнецов Алексей Дмитриевич", "ИСТ-25", 19, 4.1),
        Student("Смирнова Ольга Викторовна", "ЭК-23", 21, 3.5),
        ExcellentStudent("Орлова Елена Александрова", "ИСТ-24", 19, 4.95, scholarship=2500),
        ExcellentStudent("Волков Дмитрий Алексеевич", "ИСТ-24", 20, 4.8, scholarship=2200),
    ]


def input_int(prompt: str) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        raise ValueError("Необходимо ввести целое число")


def input_float(prompt: str) -> float:
    try:
        return float(input(prompt))
    except ValueError:
        raise ValueError("Необходимо ввести число")


def show_all(students: list) -> None:
    if not students:
        print("Список студентов пуст.")
        return
    print("\n--- Все студенты ---")
    for s in students:
        print(s)


def filter_by_grade(students: list) -> None:
    threshold = input_float("Минимальный балл (строго больше): ")
    result = students_with_grade_above(students, threshold)
    print(f"\nНайдено {len(result)} студентов:")
    for s in result:
        print(s)


def show_full_names(students: list) -> None:
    print("\nФИО студентов (map):")
    for name in full_names(students):
        print(" -", name)


def show_sorted(students: list) -> None:
    print("\nСортировка по среднему баллу (убывание):")
    for s in sort_by_grade(students, reverse=True):
        print(s)


def show_statistics(students: list) -> None:
    print(f"\nСредний балл по всем: {average_grade(students):.2f}")
    print(f"Баллы (comprehension): {grades_list(students)}")
    print(f"Группы (set comprehension): {sorted(unique_groups(students))}")
    print(f"Студентов по группам (dict comprehension): {group_to_count(students)}")

    group = input("Средний балл по группе (введите группу): ").strip()
    try:
        print(f"Средний балл группы {group}: {average_grade_of_group(students, group):.2f}")
    except ZeroDivisionError:
        print(f"Группа {group} не найдена.")


def check_conditions(students: list) -> None:
    threshold = input_float("Порог для отличника (по умолчанию 4.5): ")
    print(f"Есть ли отличник (any): {has_excellent_student(students, threshold)}")

    min_age = input_int("Все ли старше возраста: ")
    print(f"Все старше {min_age} (all): {all_older_than(students, min_age)}")


def run_generator(students: list) -> None:
    print("\n1) Генератор студентов группы")
    print("2) Генераторное выражение: квадраты баллов")
    print("3) Собственный итератор (next вручную)")
    choice = input("Выбор: ").strip()

    if choice == "1":
        group = input("Группа: ").strip()
        found = False
        for s in students_by_group(students, group):
            found = True
            print(s)
        if not found:
            print("В группе нет студентов.")
    elif choice == "2":
        print("Квадраты баллов:", [round(x, 3) for x in grade_squares(students)])
    elif choice == "3":
        iterator = StudentIterator(students)
        try:
            print("Первый:", next(iterator))
            print("Второй:", next(iterator))
        except StopIteration:
            print("Элементов нет.")
        exhausted = 0
        try:
            while True:
                next(iterator)
                exhausted += 1
        except StopIteration:
            print(f"Итератор исчерпан после ещё {exhausted} элементов (StopIteration).")
    else:
        print("Неизвестный пункт.")


def run_pipeline(students: list) -> None:
    """Демонстрация конвейера filter -> map -> sorted (доп. задание)."""
    print("\nКонвейер: балл > 4.0 -> ФИО в верхнем регистре -> сортировка по имени")
    result = process(
        students,
        predicate=lambda s: s.grade > 4.0,
        transform=lambda s: s.full_name.upper(),
        key_function=lambda name: name,
    )
    for name in result:
        print(" -", name)


def demonstrate_laziness() -> None:
    n = 1_000_000
    list_result = [x * x for x in range(n)]
    gen_result = (x * x for x in range(n))
    print(f"\nСписок: {sys.getsizeof(list_result):,} байт (все {n} элементов в памяти)")
    print(f"Генератор: {sys.getsizeof(gen_result):,} байт (элементы вычисляются лениво)")
    print("Первые 5 из генератора:", [next(gen_result) for _ in range(5)])
    del list_result


# ---------- Главное меню ----------

MENU = """
================ МЕНЮ ================
1. Показать всех студентов
2. Отфильтровать по среднему баллу (filter)
3. Показать ФИО (map)
4. Отсортировать по среднему баллу (sorted key)
5. Статистика (comprehension, reduce, any/all)
6. Проверить условия (any / all)
7. Запустить генератор / итератор
8. Конвейер обработки (filter -> map -> sorted)
9. Демонстрация ленивости (list vs generator)
0. Выход
======================================
"""


def main() -> None:
    students = build_demo_students()
    print(f"Загружено студентов: {len(students)}")

    handlers = {
        "1": show_all,
        "2": filter_by_grade,
        "3": show_full_names,
        "4": show_sorted,
        "5": show_statistics,
        "6": check_conditions,
        "7": run_generator,
        "8": run_pipeline,
        "9": lambda _: demonstrate_laziness(),
    }

    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()

        if choice == "0":
            print("Выход.")
            break

        handler = handlers.get(choice)
        if handler is None:
            print("Ошибка: неизвестный пункт меню.")
            continue

        try:
            handler(students)
        except ValueError as exc:
            print(f"Ошибка ввода: {exc}")
        except ZeroDivisionError:
            print("Ошибка: деление на ноль (пустая выборка).")
        except Exception as exc:  # страховка — программа не падает
            print(f"Непредвиденная ошибка: {exc}")


if __name__ == "__main__":
    main()