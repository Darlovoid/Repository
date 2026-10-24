from functools import reduce
from typing import Callable, Iterable, Iterator


def filter_students(students: Iterable, predicate: Callable) -> Iterator:
    return filter(predicate, students)


def transform_students(students: Iterable, operation: Callable) -> Iterator:
    return map(operation, students)


def sort_students(students: Iterable, key_function: Callable,
                  reverse: bool = False) -> list:
    return sorted(students, key=key_function, reverse=reverse)


def aggregate_students(students: Iterable, initial, operation: Callable):
    return reduce(operation, students, initial)


def students_with_grade_above(students: Iterable, threshold: float) -> list:
    return list(filter_students(students, lambda s: s.grade > threshold))


def full_names(students: Iterable) -> list:
    """Получение списка ФИО через map + lambda."""
    return list(transform_students(students, lambda s: s.full_name))


def sort_by_grade(students: Iterable, reverse: bool = True) -> list:
    return sort_students(students, key_function=lambda s: s.grade, reverse=reverse)


def average_grade(students: Iterable) -> float:
    students = list(students)
    if not students:
        return 0.0
    total = aggregate_students(students, 0.0, lambda acc, s: acc + s.grade)
    return total / len(students)


def average_grade_of_group(students: Iterable, group: str) -> float:
    in_group = list(filter_students(students, lambda s: s.group == group))
    return average_grade(in_group)


def has_excellent_student(students: Iterable, threshold: float = 4.5) -> bool:
    return any(s.grade >= threshold for s in students)


def all_older_than(students: Iterable, min_age: int) -> bool:
    students = list(students)
    if not students:
        return True
    return all(s.age > min_age for s in students)


def grades_list(students: Iterable) -> list:
    return [s.grade for s in students]


def group_to_count(students: Iterable) -> dict:
    return {group: sum(1 for s in students if s.group == group)
            for group in {s.group for s in students}}


def unique_groups(students: Iterable) -> set:
    return {s.group for s in students}


def process(students: Iterable, predicate: Callable,
            transform: Callable, key_function: Callable) -> list:
    
    return sorted(
        transform_students(filter_students(students, predicate), transform),
        key=key_function,
    )