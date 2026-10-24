from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class StudentStatus(Enum):
    ACTIVE = "активен"
    ACADEMIC_LEAVE = "академический отпуск"
    GRADUATED = "выпускник"


@dataclass
class Teacher:
    teacher_id: int
    name: str
    department: str = "общая кафедра"

    def get_report_data(self) -> str:
        return f"Преподаватель #{self.teacher_id}: {self.name} ({self.department})"


@dataclass
class Discipline:
    discipline_id: int
    name: str
    teacher_id: Optional[int] = None
    credits: int = 3

    def get_report_data(self) -> str:
        teacher = f"преподаватель #{self.teacher_id}" if self.teacher_id else "не назначен"
        return (f"Дисциплина #{self.discipline_id}: '{self.name}' | "
                f"{teacher} | кредиты: {self.credits}")


@dataclass
class Student:
    student_id: int
    name: str
    group: str = ""
    status: StudentStatus = StudentStatus.ACTIVE
    grades: dict[int, list[int]] = field(default_factory=dict)

    def get_report_data(self) -> str:
        return (f"Студент #{self.student_id}: {self.name} | "
                f"группа: {self.group or '—'} | "
                f"статус: {self.status.value}")

    def add_grade(self, discipline_id: int, grade: int) -> None:
        if not 2 <= grade <= 5:
            from exceptions import InvalidGradeError
            raise InvalidGradeError(f"Оценка должна быть от 2 до 5, получено {grade}")
        self.grades.setdefault(discipline_id, []).append(grade)

    def average_grade(self) -> Optional[float]:
        """Средний балл по всем дисциплинам. None, если оценок нет."""
        all_grades = [g for marks in self.grades.values() for g in marks]
        if not all_grades:
            return None
        return sum(all_grades) / len(all_grades)

    def has_debt(self, passing_grade: int = 3) -> bool:
        for marks in self.grades.values():
            if not marks:
                continue
            if marks[-1] < passing_grade:
                return True
        return False

    def change_status(self, new_status: StudentStatus) -> None:
        if self.status == new_status:
            return

        forbidden = {
            StudentStatus.GRADUATED: {StudentStatus.ACTIVE, StudentStatus.ACADEMIC_LEAVE},
        }
        if new_status in forbidden.get(self.status, set()):
            from exceptions import InvalidStatusTransitionError
            raise InvalidStatusTransitionError(
                f"Нельзя перейти из «{self.status.value}» в «{new_status.value}»"
            )
        self.status = new_status