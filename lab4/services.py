from typing import List, Optional

from exceptions import StudentNotFoundError
from models import Student


class StudentService:

    def __init__(self, students: Optional[List[Student]] = None):
        self.students: List[Student] = students if students is not None else []

    def add(self, student: Student) -> None:
        self.students.append(student)

    def find_by_name(self, full_name: str) -> Student:
        for student in self.students:
            if student.full_name.lower() == full_name.lower():
                return student
        raise StudentNotFoundError(full_name)

    def update(
        self,
        full_name: str,
        *,
        new_age: Optional[int] = None,
        new_group: Optional[str] = None,
        new_grade: Optional[float] = None,
    ) -> Student:
        student = self.find_by_name(full_name)

        if new_age is not None:
            student.age = new_age
        if new_group is not None:
            student.group = new_group
        if new_grade is not None:
            student.grade = new_grade

        student.validate()
        return student

    def remove(self, full_name: str) -> Student:
        student = self.find_by_name(full_name)
        self.students.remove(student)
        return student


    def average_grade(self) -> float:
        if not self.students:
            return 0.0
        return sum(s.grade for s in self.students) / len(self.students)

    def list_all(self) -> List[Student]:
        return list(self.students)