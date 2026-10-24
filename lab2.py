def input_int(message, predicate):
    while True:
        try:
            r = int(input(message + ": "))
        except:
            print("! Введите целое число")
            continue
        if predicate(r) == False:
            print("! Неправильное число")
            continue
        break
    return r


def input_float(message, predicate):
    while True:
        try:
            r = float(input(message + ": "))
        except:
            print("! Введите число")
            continue
        if predicate(r) == False:
            print("! Неправильное число")
            continue
        break
    return r


def find_by_group(students):
    group = input("Введите группу: ")
    found = list(filter(lambda x: group.lower() in x["group"].lower(), students))
    if found:
        for student in found:
            print(student)
    else:
        print("! Студенты не найдены")


def find_by_average_mark(students):
    mark = input_float("Введите минимальный средний балл", lambda x: 0 <= x <= 5)
    found = list(filter(lambda x: x["average_mark"] > mark, students))
    if found:
        for student in found:
            print(student)
    else:
        print("! Студенты не найдены")


def group_average_mark(students):
    group = input("Введите группу: ")
    marks = list(map(lambda x: x["average_mark"],
                     filter(lambda x: group.lower() in x["group"].lower(), students)))
    if marks:
        print(f"Средний балл группы {group}: {sum(marks) / len(marks):.2f}")
    else:
        print("! Студенты не найдены")


def best_and_worst_students(students):
    if not students:
        print("! Список студентов пуст")
        return

    best = max(students, key=lambda x: x["average_mark"])
    worst = min(students, key=lambda x: x["average_mark"])

    print("Лучший студент:")
    print(best)
    print("Худший студент:")
    print(worst)


def unique_groups(students):
    groups = set(map(lambda x: x["group"], students))
    print("Список уникальных учебных групп:", groups)


def sort_by_average_mark(students):
    sorted_students = sorted(students, key=lambda x: -x["average_mark"])
    for student in sorted_students:
        print(student)


def main():
    students = [{
            "full_name": "Азаров Кирилл Дмитриевич",
            "age": 20,
            "group": "ИСТ-24",
            "average_mark": 4.5,
        }, {
            "full_name": "Малюков Дмитрий Георгиевич",
            "age": 19,
            "group": "ИИ-25",
            "average_mark": 3.8,
        }, {
            "full_name": "Сидорова Анна Петровна",
            "age": 18,
            "group": "ИИ-25",
            "average_mark": 4.9,
        }, {
            "full_name": "Кузнецов Алексей Дмитриевич",
            "age": 19,
            "group": "ИСТ-25",
            "average_mark": 4.1,
        }, {
            "full_name": "Смирнова Ольга Викторовна",
            "age": 21,
            "group": "ЭК-23",
            "average_mark": 3.5,
        }
    ]

    menu = """
=============== МЕНЮ ===============
1. Все студенты
2. Найти студентов заданной группы
3. Найти студентов со средним баллом выше заданного
4. Определить средний балл группы
5. Найти лучшего и худшего студента
6. Вывести список уникальных учебных групп
7. Отсортировать студентов по среднему баллу
0. Выход
====================================
"""

    while True:
        print(menu)

        p = input_int("Введите опцию", lambda p: 0 <= p <= 9)
        match p:
            case 1:
                for student in students:
                    print(student)
            case 2:
                find_by_group(students)
            case 3:
                find_by_average_mark(students)
            case 4:
                group_average_mark(students)
            case 5:
                best_and_worst_students(students)
            case 6:
                unique_groups(students)
            case 7:
                sort_by_average_mark(students)
            case 0:
                break

        input("Нажмите Enter, чтобы продолжить")


if __name__ == "__main__":
    main()
