class StudentNotFoundError(Exception):

    def __init__(self, query: str):
        self.query = query
        super().__init__(f"Студент не найден: {query}")


class InvalidStudentDataError(Exception):

    def __init__(self, message: str):
        super().__init__(f"Некорректные данные студента: {message}")