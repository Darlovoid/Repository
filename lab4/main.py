import os
import sys

from exceptions import InvalidStudentDataError, StudentNotFoundError
from models import Student
from services import StudentService
from storage import StudentStorage

DATA_DIR = "data"
JSON_PATH = os.path.join(DATA_DIR, "students.json")
CSV_PATH = os.path.join(DATA_DIR, "students.csv")


def input_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: необходимо ввести число.")


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")


def action_add(service: StudentService) -> None:
    print("\n--- Добавление студента ---")
    try:
        student = Student(
            full_name=input_non_empty("ФИО: "),
            age=input_int("Возраст: "),
            group=input_non_empty("Группа: "),
            grade=input_float("Средний балл: "),
        )
    except InvalidStudentDataError as error:
        print(f"Не удалось добавить студента: {error}")
        return
    service.add(student)
    print("Студент добавлен.")


def action_list(service: StudentService) -> None:
    print("\n--- Список студентов ---")
    students = service.list_all()
    if not students:
        print("Список пуст.")
        return
    for i, student in enumerate(students, start=1):
        print(f"{i}. {student}")
    print(f"Средний балл по всем: {service.average_grade():.2f}")


def action_find(service: StudentService) -> None:
    print("\n--- Поиск студента ---")
    name = input_non_empty("ФИО: ")
    try:
        student = service.find_by_name(name)
    except StudentNotFoundError as error:
        print(f"Ошибка: {error}")
        return
    print(f"Найден: {student}")


def action_update(service: StudentService) -> None:
    print("\n--- Изменение данных студента ---")
    name = input_non_empty("ФИО студента: ")

    print("Оставьте поле пустым, чтобы не менять его.")
    new_age_raw = input("Новый возраст: ").strip()
    new_group_raw = input("Новая группа: ").strip()
    new_grade_raw = input("Новый средний балл: ").strip()

    try:
        service.update(
            name,
            new_age=int(new_age_raw) if new_age_raw else None,
            new_group=new_group_raw or None,
            new_grade=(
                float(new_grade_raw.replace(",", ".")) if new_grade_raw else None
            ),
        )
    except StudentNotFoundError as error:
        print(f"Ошибка: {error}")
    except (ValueError, InvalidStudentDataError) as error:
        print(f"Ошибка: {error}")
    else:
        print("Данные обновлены.")


def action_remove(service: StudentService) -> None:
    print("\n--- Удаление студента ---")
    name = input_non_empty("ФИО: ")
    try:
        removed = service.remove(name)
    except StudentNotFoundError as error:
        print(f"Ошибка: {error}")
    else:
        print(f"Удалён: {removed}")


def action_save(service: StudentService, storage: StudentStorage) -> None:
    print("\n--- Сохранение в JSON ---")
    try:
        storage.save_json(service.list_all())
    except OSError as error:
        print(f"Ошибка сохранения: {error}")
    else:
        print(f"Сохранено в {storage.json_path}")


def action_export_csv(service: StudentService, storage: StudentStorage) -> None:
    print("\n--- Экспорт в CSV ---")
    try:
        storage.export_csv(service.list_all())
    except OSError as error:
        print(f"Ошибка экспорта: {error}")
    else:
        print(f"Экспортировано в {storage.csv_path}")


def action_load(service: StudentService, storage: StudentStorage) -> None:
    print("\n--- Загрузка из JSON ---")
    try:
        students = storage.load_json()
    except FileNotFoundError:
        print("Файл не найден — будет создан при первом сохранении.")
        return
    except (ValueError, KeyError, TypeError) as error:
        print(f"Ошибка чтения JSON: {error}")
        return

    service.students = students
    print(f"Загружено студентов: {len(students)}")


def main() -> None:
    storage = StudentStorage(JSON_PATH, CSV_PATH)

    try:
        service = StudentService(storage.load_json())
        print(f"Автозагрузка выполнена. Студентов: {len(service.students)}")
    except (ValueError, KeyError, TypeError) as error:
        print(f"Не удалось загрузить данные ({error}). Начинаем с пустого списка.")
        service = StudentService()



    menu = """
===== УЧЁТ СТУДЕНТОВ =====
1. Показать всех студентов
2. Добавить студента
3. Найти студента по ФИО
4. Изменить данные студента
5. Удалить студента
6. Показать средний балл
7. Сохранить в JSON
8. Экспортировать в CSV
9. Загрузить из JSON
0. Выход
===========================
"""

    while True:
        print(menu)
        choice = input("Выберите пункт: ").strip()

        actions = {
        "1": lambda: action_list(service),
        "2": lambda: action_add(service),
        "3": lambda: action_find(service),
        "4": lambda: action_update(service),
        "5": lambda: action_remove(service),
        "6": lambda: print(f"\nСредний балл: {service.average_grade():.2f}"),
        "7": lambda: action_save(service, storage),
        "8": lambda: action_export_csv(service, storage),
        "9": lambda: action_load(service, storage),
    }

        if choice == "0":
            try:
                storage.save_json(service.list_all())
                print(f"Данные сохранены в {storage.json_path}")
            except OSError as error:
                print(f"Не удалось сохранить данные: {error}")
            print("Выход.")
            break

        action = actions.get(choice)
        if action is None:
            print("Неизвестный пункт меню. Повторите ввод.")
            continue

        try:
            action()
        except Exception as error:
            print(f"Непредвиденная ошибка: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
        sys.exit(0)