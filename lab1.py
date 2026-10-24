def input_students():
    while True:
        count = int(input("Введите количество студентов: "))
        if count <= 0:
            print("Ошибка: количество студентов должно быть положительным.")
        else:
            break

    grades = []

    for i in range(count):
        while True:
            grade = int(input(f"Введите оценку студента {i + 1} (2–5): "))
            if 2 <= grade <= 5:
                grades.append(grade)
                break
            else:
                print("Ошибка: оценка должна быть в диапазоне от 2 до 5.")

    return grades


def calculate_average(grades):
    total = 0
    for grade in grades:
        total += grade
    return total / len(grades)


def count_by_grade(grades):
    counts = {2: 0, 3: 0, 4: 0, 5: 0}
    for grade in grades:
        counts[grade] += 1
    return counts


def count_failing(grades):
    failing = 0
    for grade in grades:
        if grade == 2:
            failing += 1
    return failing


def find_max_min(grades):
    maximum = grades[0]
    minimum = grades[0]

    for grade in grades:
        if grade > maximum:
            maximum = grade
        if grade < minimum:
            minimum = grade

    return maximum, minimum


def get_group_characteristic(average):
    if average >= 4.5:
        return "Отличная успеваемость"
    elif average >= 3.5:
        return "Хорошая успеваемость"
    elif average >= 2.5:
        return "Удовлетворительная успеваемость"
    else:
        return "Низкая успеваемость, требуется внимание"


def print_results(grades):
    average = calculate_average(grades)
    counts = count_by_grade(grades)
    failing = count_failing(grades)
    maximum, minimum = find_max_min(grades)
    characteristic = get_group_characteristic(average)

    print("\n===== Результаты анализа =====")
    print(f"Количество студентов: {len(grades)}")
    print(f"Средний балл: {average:.2f}")
    print(f"Максимальная оценка: {maximum}")
    print(f"Минимальная оценка: {minimum}")
    print(f"Количество неуспевающих студентов: {failing}")
    print("\nКоличество студентов с каждой оценкой:")
    print(f"  Оценка 5: {counts[5]}")
    print(f"  Оценка 4: {counts[4]}")
    print(f"  Оценка 3: {counts[3]}")
    print(f"  Оценка 2: {counts[2]}")
    print(f"\nХарактеристика группы: {characteristic}")


def main():
    print("=== Анализ успеваемости студентов ===")
    grades = input_students()
    print_results(grades)


if __name__ == "__main__":
    main()