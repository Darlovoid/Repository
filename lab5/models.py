class Person:

    def __init__(self, full_name: str, age: int):
        if not full_name or not full_name.strip():
            raise ValueError("ФИО не может быть пустым")
        if age < 0 or age > 120:
            raise ValueError("Возраст должен быть в диапазоне 0..120")
        self._full_name = full_name.strip()
        self._age = age

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def age(self) -> int:
        return self._age

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._full_name!r}, age={self._age})"


class Student(Person):

    def __init__(self, full_name: str, group: str, age: int, grade: float):
        super().__init__(full_name, age)
        if not group or not group.strip():
            raise ValueError("Группа не может быть пустой")
        if not (0.0 <= grade <= 5.0):
            raise ValueError("Средний балл должен быть в диапазоне 0..5")
        self._group = group.strip()
        self._grade = float(grade)

    @property
    def group(self) -> str:
        return self._group

    @property
    def grade(self) -> float:
        return self._grade

    def to_dict(self) -> dict:
        return {
            "type": "Student",
            "full_name": self._full_name,
            "group": self._group,
            "age": self._age,
            "grade": self._grade,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            data["full_name"],
            data["group"],
            int(data["age"]),
            float(data["grade"]),
        )

    def __str__(self) -> str:
        return (
            f"{self._full_name:<25} | группа {self._group:<8} | "
            f"возраст {self._age:>3} | балл {self._grade:.2f}"
        )


class ExcellentStudent(Student):

    def __init__(self, full_name: str, group: str, age: int, grade: float,
                 scholarship: float = 0.0):
        super().__init__(full_name, group, age, grade)
        if scholarship < 0:
            raise ValueError("Стипендия не может быть отрицательной")
        self._scholarship = float(scholarship)

    @property
    def scholarship(self) -> float:
        return self._scholarship

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "ExcellentStudent"
        data["scholarship"] = self._scholarship
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "ExcellentStudent":
        return cls(
            data["full_name"],
            data["group"],
            int(data["age"]),
            float(data["grade"]),
            float(data.get("scholarship", 0.0)),
        )

    def __str__(self) -> str:
        return super().__str__() + f" | стипендия {self._scholarship:.0f}"


STUDENT_TYPES = {
    "Student": Student,
    "ExcellentStudent": ExcellentStudent,
}


def student_from_dict(data: dict) -> Student:
    cls = STUDENT_TYPES.get(data.get("type", "Student"), Student)
    return cls.from_dict(data)