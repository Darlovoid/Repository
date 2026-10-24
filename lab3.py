from abc import ABC, abstractmethod


class Person(ABC):

    university = "ИТ-университет"

    def __init__(self, full_name, age):
        self._full_name = full_name 
        self._age = age               

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if not value or not value.strip():
            raise ValueError("ФИО не может быть пустым")
        self._full_name = value.strip()

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 16 or value > 100:
            raise ValueError("Возраст должен быть в диапазоне 16..100")
        self._age = value

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_characteristic(self):
        pass

    def update_data(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return self.get_info()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._full_name!r})"


class Student(Person):

    def __init__(self, full_name, age, group, average_grade):
        super().__init__(full_name, age)   # вызов конструктора базового класса
        self.group = group
        self._average_grade = average_grade

    @property
    def average_grade(self):
        return self._average_grade

    @average_grade.setter
    def average_grade(self, value):
        if not (0 <= value <= 5):
            raise ValueError("Средний балл должен быть в диапазоне 0..5")
        self._average_grade = value

    def get_info(self):
        return (f"[Студент] {self.full_name}, возраст: {self.age}, "
                f"группа: {self.group}, средний балл: {self.average_grade:.2f}")

    def get_characteristic(self):
        if self._average_grade >= 4.5:
            return "Отличник"
        elif self._average_grade >= 3.5:
            return "Хорошист"
        elif self._average_grade >= 2.5:
            return "Троечник"
        else:
            return "Неуспевающий"

    def change_group(self, new_group):
        self.group = new_group


class Teacher(Person):

    def __init__(self, full_name, age, department, position, experience):
        super().__init__(full_name, age)
        self.department = department
        self.position = position
        self._experience = experience

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        if value < 0:
            raise ValueError("Стаж не может быть отрицательным")
        self._experience = value

    def get_info(self):
        return (f"[Преподаватель] {self.full_name}, возраст: {self.age}, "
                f"кафедра: {self.department}, должность: {self.position}, "
                f"стаж: {self.experience} лет")

    def get_characteristic(self):
        if self._experience >= 20:
            return "Профессор"
        elif self._experience >= 10:
            return "Доцент"
        elif self._experience >= 3:
            return "Старший преподаватель"
        else:
            return "Ассистент"

    def promote(self, new_position):
        self.position = new_position


class University:

    def __init__(self, name):
        self.name = name
        self._people = []

    def add_person(self, person):
        if not isinstance(person, Person):
            raise TypeError("Можно добавлять только объекты Person")
        self._people.append(person)

    def remove_person(self, index):
        if 0 <= index < len(self._people):
            return self._people.pop(index)
        raise IndexError("Некорректный индекс")

    def show_all(self):
        if not self._people:
            print("  Список пуст.")
            return
        for i, person in enumerate(self._people):
            print(f"  {i}. {person.get_info()}")

    def get_polymorphic_info(self):
        print("\n--- Полиморфный вывод (get_info) ---")
        for person in self._people:
            print(" ", person.get_info())

    def get_polymorphic_characteristics(self):
        print("\n--- Полиморфный вывод (get_characteristic) ---")
        for person in self._people:
            print(f"  {person.full_name}: {person.get_characteristic()}")

    def statistics(self):
        students = [p for p in self._people if isinstance(p, Student)]
        teachers = [p for p in self._people if isinstance(p, Teacher)]

        print(f"\n--- Статистика {self.name} ---")
        print(f"  Всего человек: {len(self._people)}")
        print(f"  Студентов: {len(students)}")
        print(f"  Преподавателей: {len(teachers)}")

        if students:
            avg = sum(s.average_grade for s in students) / len(students)
            print(f"  Средний балл студентов: {avg:.2f}")

        if teachers:
            avg_exp = sum(t.experience for t in teachers) / len(teachers)
            print(f"  Средний стаж преподавателей: {avg_exp:.1f} лет")

    def find_by_name(self, substring):
        result = [p for p in self._people
                  if substring.lower() in p.full_name.lower()]
        return result


def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Ошибка: введите целое число.")


def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Ошибка: введите число.")


def create_student():
    print("\n--- Создание студента ---")
    name = input("ФИО: ")
    age = input_int("Возраст: ")
    group = input("Группа: ")
    grade = input_float("Средний балл: ")
    try:
        return Student(name, age, group, grade)
    except ValueError as e:
        print(f"  Ошибка: {e}")
        return None


def create_teacher():
    print("\n--- Создание преподавателя ---")
    name = input("ФИО: ")
    age = input_int("Возраст: ")
    dept = input("Кафедра: ")
    pos = input("Должность: ")
    exp = input_int("Стаж (лет): ")
    try:
        return Teacher(name, age, dept, pos, exp)
    except ValueError as e:
        print(f"  Ошибка: {e}")
        return None


def change_object(university):
    print("\n--- Изменение объекта ---")
    university.show_all()
    if not university._people:
        return
    idx = input_int("Введите номер объекта: ")
    if not (0 <= idx < len(university._people)):
        print("  Некорректный номер.")
        return
    person = university._people[idx]
    print(f"  Выбран: {person.get_info()}")
    print("  Что изменить?")
    print("    1. ФИО")
    print("    2. Возраст")
    if isinstance(person, Student):
        print("    3. Группа")
        print("    4. Средний балл")
    elif isinstance(person, Teacher):
        print("    3. Кафедра")
        print("    4. Должность")
        print("    5. Стаж")
    choice = input_int("  Ваш выбор: ")
    try:
        if choice == 1:
            person.full_name = input("Новое ФИО: ")
        elif choice == 2:
            person.age = input_int("Новый возраст: ")
        elif choice == 3:
            if isinstance(person, Student):
                person.group = input("Новая группа: ")
            elif isinstance(person, Teacher):
                person.department = input("Новая кафедра: ")
        elif choice == 4:
            if isinstance(person, Student):
                person.average_grade = input_float("Новый средний балл: ")
            elif isinstance(person, Teacher):
                person.position = input("Новая должность: ")
        elif choice == 5 and isinstance(person, Teacher):
            person.experience = input_int("Новый стаж: ")
        else:
            print("  Некорректный выбор.")
            return
        print("  Данные обновлены.")
    except ValueError as e:
        print(f"  Ошибка: {e}")


def delete_object(university):
    print("\n--- Удаление объекта ---")
    university.show_all()
    if not university._people:
        return
    idx = input_int("Введите номер для удаления: ")
    try:
        removed = university.remove_person(idx)
        print(f"  Удалён: {removed.full_name}")
    except IndexError as e:
        print(f"  Ошибка: {e}")


def search_objects(university):
    print("\n--- Поиск по ФИО ---")
    substr = input("Введите подстроку: ")
    results = university.find_by_name(substr)
    if results:
        for p in results:
            print("  ", p.get_info())
    else:
        print("  Ничего не найдено.")


def main():
    uni = University("ИТ-университет")
    uni.add_person(Student("Азаров Кирилл Дмитриевич", 20, "ИСТ-24", 3.9))
    uni.add_person(Student("Малюков Дмитрий Георгиевич", 19, "ИИ-24", 3.8))
    uni.add_person(Teacher("Сидоров Пётр Николаевич", 45,
                           "Информатики", "Доцент", 15))
    uni.add_person(Teacher("Калашникова Мария Ивановна", 39,
                           "Математики", "Профессор", 30))

    menu = """
=============== МЕНЮ ===============
1. Создать объект (студент/преподаватель)
2. Показать объекты (get_info)
3. Показать характеристику (get_characteristic)
4. Изменить объект
5. Удалить объект
6. Показать статистику
7. Поиск по ФИО
0. Выход
====================================
"""

    while True:
        print(menu)
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            print("  1. Студент")
            print("  2. Преподаватель")
            t = input_int("  Тип: ")
            if t == 1:
                obj = create_student()
            elif t == 2:
                obj = create_teacher()
            else:
                print("  Некорректный тип.")
                continue
            if obj:
                uni.add_person(obj)
                print("  Объект добавлен.")

        elif choice == "2":
            uni.get_polymorphic_info()

        elif choice == "3":
            uni.get_polymorphic_characteristics()

        elif choice == "4":
            change_object(uni)

        elif choice == "5":
            delete_object(uni)

        elif choice == "6":
            uni.statistics()

        elif choice == "7":
            search_objects(uni)

        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Некорректный пункт меню.")


if __name__ == "__main__":
    main()