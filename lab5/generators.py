from typing import Iterable, Iterator


def students_by_group(students: Iterable, group: str) -> Iterator:
    for student in students:
        if student.group == group:
            yield student


def grade_squares(students: Iterable) -> Iterator:
    return (s.grade ** 2 for s in students)


class StudentIterator:

    def __init__(self, students: Iterable):
        self._students = list(students)
        self._index = 0

    def __iter__(self) -> "StudentIterator":
        return self

    def __next__(self):
        if self._index >= len(self._students):
            raise StopIteration
        student = self._students[self._index]
        self._index += 1
        return student