import csv
import json
import os
from typing import Iterable, List

from models import Student


class StudentStorage:

    def __init__(self, json_path: str, csv_path: str):
        self.json_path = json_path
        self.csv_path = csv_path


    def save_json(self, students: Iterable[Student]) -> None:
        """Сохранить список студентов в JSON."""
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        data = [student.to_dict() for student in students]
        with open(self.json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_json(self) -> List[Student]:
        if not os.path.exists(self.json_path):
            return []

        with open(self.json_path, "r", encoding="utf-8") as file:
            raw = json.load(file)

        if not isinstance(raw, list):
            raise ValueError("Ожидался список студентов в JSON-файле")

        return [Student.from_dict(item) for item in raw]

    def export_csv(self, students: Iterable[Student]) -> None:
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        with open(self.csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["full_name", "age", "group", "grade"])
            for student in students:
                writer.writerow([
                    student.full_name,
                    student.age,
                    student.group,
                    student.grade,
                ])