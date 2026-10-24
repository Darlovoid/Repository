import inspect
from models import *
from exceptions import *
from decorators import *
from protocols import Reportable


class UniversityService:
    def __init__(self):
        self._students: list[Student] = []
        self._teachers: list[Teacher] = []
        self._disciplines: list[Discipline] = []

    @log_call
    def add_student(self, student: Student) -> Student:
        self._students.append(student)
        return student

    @log_call
    def add_teacher(self, teacher: Teacher) -> Teacher:
        self._teachers.append(teacher)
        return teacher

    @log_call
    def add_discipline(self, discipline: Discipline) -> Discipline:
        self._disciplines.append(discipline)
        return discipline

    def find_student(self, student_id: int) -> Student:
        for s in self._students:
            if s.student_id == student_id:
                return s
        raise StudentNotFoundError(f"Студент #{student_id} не найден")

    def find_teacher(self, teacher_id: int) -> Teacher:
        for t in self._teachers:
            if t.teacher_id == teacher_id:
                return t
        raise TeacherNotFoundError(f"Преподаватель #{teacher_id} не найден")

    def find_discipline(self, discipline_id: int) -> Discipline:
        for d in self._disciplines:
            if d.discipline_id == discipline_id:
                return d
        raise DisciplineNotFoundError(f"Дисциплина #{discipline_id} не найдена")

    @log_call
    def assign_teacher(self, discipline_id: int, teacher_id: int) -> Discipline:
        discipline = self.find_discipline(discipline_id)
        teacher = self.find_teacher(teacher_id)
        discipline.teacher_id = teacher.teacher_id
        print(f"Дисциплина #{discipline_id} закреплена за {teacher.name}")
        return discipline

    @log_call
    def add_grade(self, student_id: int, discipline_id: int, grade: int) -> Student:
        student = self.find_student(student_id)
        self.find_discipline(discipline_id)
        student.add_grade(discipline_id, grade)
        print(f"Студенту {student.name} выставлена оценка {grade} "
              f"по дисциплине #{discipline_id}")
        return student

    @measure_time
    def get_students_with_debts(self) -> list[Student]:
        return [s for s in self._students
                if s.status == StudentStatus.ACTIVE and s.has_debt()]

    @repeat(1)
    def get_average_by_student(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for s in self._students:
            avg = s.average_grade()
            if avg is not None:
                result[s.name] = round(avg, 2)
        return result

    def get_average_by_discipline(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for d in self._disciplines:
            marks = [g for s in self._students for g in s.grades.get(d.discipline_id, [])]
            if marks:
                result[d.name] = round(sum(marks) / len(marks), 2)
        return result

    def get_statistics(self) -> dict:
        return {
            "total_students": len(self._students),
            "by_status": {
                st.value: sum(1 for s in self._students if s.status == st)
                for st in StudentStatus
            },
            "with_debts": len(self.get_students_with_debts()),
            "total_disciplines": len(self._disciplines),
            "total_teachers": len(self._teachers),
        }

    def inspect_object(self, obj) -> None:
        print(f"\n=== ИНФОРМАЦИЯ ОБ ОБЪЕКТЕ ===")
        # 1. type()
        print(f"Тип: {type(obj).__name__}")
        # 2. isinstance() + issubclass() (structural check через Protocol)
        for cls_name, cls in [("Student", Student), ("Teacher", Teacher),
                              ("Discipline", Discipline)]:
            if isinstance(obj, cls):
                print(f"isinstance({cls_name}): True")
                print(f"Reportable (structural): {isinstance(obj, Reportable)}")
        # 3. dir() / hasattr() / getattr()
        attrs = [a for a in dir(obj) if not a.startswith("__")
                 and not callable(getattr(obj, a))]
        methods = [a for a in dir(obj) if not a.startswith("__")
                   and callable(getattr(obj, a))]
        print(f"Атрибуты: {attrs}")
        print(f"Методы: {methods}")
        # 4. hasattr() + getattr()
        if hasattr(obj, "get_report_data"):
            print(f"Отчёт: {getattr(obj, 'get_report_data')()}")
        # 5. inspect.signature()
        if hasattr(obj, "change_status"):
            sig = inspect.signature(obj.change_status)
            print(f"Сигнатура change_status: {sig}")