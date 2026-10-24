from models import *
from services import UniversityService
from exceptions import UniversitySystemError
from context import OperationLogger
from protocols import Reportable
from decorators import require_status


def input_int(message: str, predicate=lambda x: True) -> int:
    while True:
        try:
            value = int(input(message + ": "))
        except ValueError:
            print("! Введите целое число")
            continue
        if not predicate(value):
            print("! Неверное значение")
            continue
        return value


def demo_protocol(obj: Reportable):
    print(f"[PROTOCOL] {obj.get_report_data()}")


@require_status(StudentStatus.ACTIVE)
def _do_grade(service, student, discipline_id: int, grade: int):
    service.add_grade(student.student_id, discipline_id, grade)


def main():
    service = UniversityService()

    with OperationLogger("Инициализация демо-данных"):
        service.add_teacher(Teacher(1, "Иванов И.И.", "каф. информатики"))
        service.add_teacher(Teacher(2, "Петрова П.П.", "каф. математики"))

        service.add_discipline(Discipline(1, "Программирование", teacher_id=1, credits=4))
        service.add_discipline(Discipline(2, "Математический анализ", teacher_id=2, credits=5))
        service.add_discipline(Discipline(3, "Базы данных", teacher_id=1, credits=3))

        s1 = Student(1, "Алексей Смирнов", "ИУ-21")
        s1.add_grade(1, 5)
        s1.add_grade(1, 4)
        s1.add_grade(2, 4)
        service.add_student(s1)

        s2 = Student(2, "Мария Кузнецова", "ИУ-21")
        s2.add_grade(1, 3)
        s2.add_grade(2, 2)
        service.add_student(s2)

        s3 = Student(3, "Сергей Попов", "ИУ-22", status=StudentStatus.ACADEMIC_LEAVE)
        s3.add_grade(1, 4)
        service.add_student(s3)

        s4 = Student(4, "Анна Волкова", "ИУ-20", status=StudentStatus.GRADUATED)
        s4.add_grade(1, 5)
        s4.add_grade(2, 5)
        service.add_student(s4)

    while True:
        print("\n1. Показать студентов")
        print("2. Показать преподавателей")
        print("3. Показать дисциплины")
        print("4. Закрепить преподавателя за дисциплиной")
        print("5. Выставить оценку студенту")
        print("6. Средний балл по студентам")
        print("7. Средний балл по дисциплинам")
        print("8. Студенты с задолженностями")
        print("9. Изменить статус студента")
        print("10. Статистика")
        print("11. Интроспекция объекта")
        print("12. Демонстрация Protocol")
        print("13. Демонстрация @require_status")
        print("0. Выход")

        choice = input_int("Выберите действие", lambda x: 0 <= x <= 13)

        try:
            match choice:
                case 1:
                    for s in service._students:
                        print(s.get_report_data())

                case 2:
                    for t in service._teachers:
                        print(t.get_report_data())

                case 3:
                    for d in service._disciplines:
                        print(d.get_report_data())

                case 4:
                    d_id = input_int("ID дисциплины", lambda x: x > 0)
                    t_id = input_int("ID преподавателя", lambda x: x > 0)
                    with OperationLogger(f"Закрепление дисциплины #{d_id}"):
                        service.assign_teacher(d_id, t_id)

                case 5:
                    s_id = input_int("ID студента", lambda x: x > 0)
                    d_id = input_int("ID дисциплины", lambda x: x > 0)
                    g = input_int("Оценка (2-5)", lambda x: 2 <= x <= 5)
                    student = service.find_student(s_id)
                    with OperationLogger(f"Выставление оценки студенту #{s_id}"):
                        _do_grade(service, student, d_id, g)

                case 6:
                    avgs = service.get_average_by_student()
                    print("\nСредний балл по студентам:")
                    for name, avg in avgs.items():
                        print(f"  {name}: {avg}")

                case 7:
                    avgs = service.get_average_by_discipline()
                    print("\nСредний балл по дисциплинам:")
                    for name, avg in avgs.items():
                        print(f"  {name}: {avg}")

                case 8:
                    debtors = service.get_students_with_debts()
                    if not debtors:
                        print("Студентов с задолженностями нет.")
                    else:
                        print(f"\nСтудентов с задолженностями: {len(debtors)}")
                        for s in debtors:
                            print(f"  {s.get_report_data()}")

                case 9:
                    s_id = input_int("ID студента", lambda x: x > 0)
                    print("Доступные статусы:")
                    for i, st in enumerate(StudentStatus, 1):
                        print(f"  {i}. {st.value}")
                    idx = input_int("Номер статуса",
                                    lambda x: 1 <= x <= len(StudentStatus))
                    new_status = list(StudentStatus)[idx - 1]
                    student = service.find_student(s_id)
                    with OperationLogger(f"Смена статуса студента #{s_id}"):
                        student.change_status(new_status)
                    print(f"Статус изменён на: «{new_status.value}»")

                case 10:
                    stats = service.get_statistics()
                    print("\nСтатистика:")
                    print(f"Всего студентов: {stats['total_students']}")
                    print("По статусам:")
                    for status, count in stats["by_status"].items():
                        print(f"  {status}: {count}")
                    print(f"С задолженностями: {stats['with_debts']}")
                    print(f"Всего дисциплин: {stats['total_disciplines']}")
                    print(f"Всего преподавателей: {stats['total_teachers']}")

                case 11:
                    print("Выберите объект для интроспекции:")
                    print("1. Студент #1")
                    print("2. Преподаватель #1")
                    print("3. Дисциплина #1")
                    obj_choice = input_int("Выбор", lambda x: 1 <= x <= 3)
                    obj = [service._students[0],
                           service._teachers[0],
                           service._disciplines[0]][obj_choice - 1]
                    service.inspect_object(obj)

                case 12:
                    print("Объекты, соответствующие Protocol Reportable:")
                    demo_protocol(service._students[0])
                    demo_protocol(service._teachers[0])
                    demo_protocol(service._disciplines[0])

                case 13:
                    s_id = input_int("ID студента", lambda x: x > 0)
                    student = service.find_student(s_id)
                    try:
                        with OperationLogger("Требуется статус ACTIVE"):
                            _do_grade(service, student, 1, 5)
                    except ValueError as e:
                        print(f"! {e}")

                case 0:
                    print("Выход.")
                    break

        except UniversitySystemError as e:
            print(f"! Ошибка системы: {e}")
        except ValueError as e:
            print(f"! Некорректные данные: {e}")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()