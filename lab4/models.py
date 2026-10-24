from exceptions import InvalidStudentDataError


class Student:

    def __init__(self, full_name: str, age: int, group: str, grade: float):
        self.full_name = full_name
        self.age = age
        self.group = group
        self.grade = grade
        self.validate()

    def validate(self) -> None:
        if not self.full_name or not isinstance(self.full_name, str):
            raise InvalidStudentDataError("ФИО не может быть пустым")
        if not isinstance(self.age, int) or self.age <= 0 or self.age > 120:
            raise InvalidStudentDataError("возраст должен быть целым числом от 1 до 120")
        if not self.group or not isinstance(self.group, str):
            raise InvalidStudentDataError("группа не может быть пустой")
        if not isinstance(self.grade, (int, float)) or not (0 <= self.grade <= 5):
            raise InvalidStudentDataError("средний балл должен быть в диапазоне 0..5")

    def to_dict(self) -> dict:
        return {
            "full_name": self.full_name,
            "age": self.age,
            "group": self.group,
            "grade": self.grade,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            full_name=data["full_name"],
            age=int(data["age"]),
            group=data["group"],
            grade=float(data["grade"]),
        )

    def __repr__(self) -> str:
        return (
            f"Student(full_name={self.full_name!r}, age={self.age}, "
            f"group={self.group!r}, grade={self.grade})"
        )

    def __str__(self) -> str:
        return (
            f"{self.full_name} | возраст: {self.age} | "
            f"группа: {self.group} | средний балл: {self.grade:.2f}"
        )