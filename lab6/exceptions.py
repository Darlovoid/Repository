class UniversitySystemError(Exception):
    pass


class StudentNotFoundError(UniversitySystemError):
    pass


class TeacherNotFoundError(UniversitySystemError):
    pass


class DisciplineNotFoundError(UniversitySystemError):
    pass


class InvalidStatusTransitionError(UniversitySystemError):
    pass


class InvalidGradeError(UniversitySystemError):
    pass