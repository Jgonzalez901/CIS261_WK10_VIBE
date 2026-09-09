"""Student record manager for test scores and calculated grades."""

import csv
from dataclasses import dataclass


@dataclass
class Student:
	"""Store one student's identifying information and test scores."""

	student_id: str
	name: str
	test1: float
	test2: float
	test3: float

	@property
	def scores(self) -> tuple[float, float, float]:
		"""Return the three test scores in test order."""
		return self.test1, self.test2, self.test3

	@property
	def average(self) -> float:
		"""Return the student's average score, or zero without scores."""
		return sum(self.scores) / 3

	@property
	def grade(self) -> str:
		"""Return a letter grade based on the student's average."""
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	@property
	def letter_grade(self) -> str:
		"""Return the calculated grade using the legacy property name."""
		return self.grade


def get_score(prompt: str) -> float:
	"""Read and validate a score from 0 through 100."""
	while True:
		try:
			score = float(input(prompt))
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a number between 0 and 100.")


def display_student(student: Student) -> None:
	"""Print one student's record in a readable format."""
	print_student_table([student])


def print_student_table(students: list[Student]) -> None:
	"""Display student records in aligned columns."""
	if not students:
		print("No student records have been added.")
		return
	header = f"{'ID':<12} {'Name':<25} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>7}"
	print(header)
	print("-" * len(header))
	for student in students:
		print(
			f"{student.student_id:<12} {student.name:<25.25} "
			f"{student.test1:>8.2f} {student.test2:>8.2f} "
			f"{student.test3:>8.2f} {student.average:>9.2f} "
			f"{student.grade:>7}"
		)


def add_student(students: dict[str, Student]) -> None:
	"""Create a student record and collect any initial test scores."""
	student_id = input("Student ID: ").strip()
	if not student_id:
		print("Student ID cannot be blank.")
		return
	if student_id in students:
		print("That student ID already exists.")
		return

	name = input("Student name: ").strip()
	if not name:
		print("Student name cannot be blank.")
		return

	test1 = get_score("Test 1 score: ")
	test2 = get_score("Test 2 score: ")
	test3 = get_score("Test 3 score: ")
	student = Student(student_id, name, test1, test2, test3)

	students[student_id] = student
	print("Student record added.")


def update_score(students: dict[str, Student]) -> None:
	"""Update one of an existing student's three test scores."""
	student_id = input("Student ID: ").strip()
	student = students.get(student_id)
	if student is None:
		print("Student not found.")
		return
	while True:
		test_number = input("Test number to update (1-3): ").strip()
		if test_number in {"1", "2", "3"}:
			break
		print("Enter 1, 2, or 3.")
	new_score = get_score(f"Test {test_number} score: ")
	if test_number == "1":
		student.test1 = new_score
	elif test_number == "2":
		student.test2 = new_score
	else:
		student.test3 = new_score
	print("Test score updated.")


def find_student(students: dict[str, Student]) -> None:
	"""Search for students by name without regard to letter case."""
	name = input("Student name: ").strip().casefold()
	matches = [student for student in students.values() if name in student.name.casefold()]
	if matches:
		print_student_table(sorted(matches, key=lambda record: record.name.casefold()))
	else:
		print("No students found with that name.")


def remove_student(students: dict[str, Student]) -> None:
	"""Delete a student record by ID."""
	student_id = input("Student ID: ").strip()
	if students.pop(student_id, None) is None:
		print("Student not found.")
	else:
		print("Student record removed.")


def show_all_students(students: dict[str, Student]) -> None:
	"""Display all records ordered by student ID."""
	print_student_table(sorted(students.values(), key=lambda record: record.student_id))


def show_statistics(students: dict[str, Student]) -> None:
	"""Display the highest, lowest, and overall class averages."""
	if not students:
		print("No student records are available for statistics.")
		return
	averages = [student.average for student in students.values()]
	highest = max(students.values(), key=lambda student: student.average)
	lowest = min(students.values(), key=lambda student: student.average)
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def save_students(students: dict[str, Student], filename: str = "student_grades.txt") -> bool:
	"""Save all student records in a portable tabular text format."""
	try:
		with open(filename, "w", newline="", encoding="utf-8") as file:
			writer = csv.writer(file, delimiter="|", lineterminator="\n")
			writer.writerow(("name", "id", "test1", "test2", "test3", "average", "grade"))
			for student in sorted(students.values(), key=lambda record: record.student_id):
				writer.writerow(
					(
						student.name,
						student.student_id,
						*(f"{score:.2f}" for score in student.scores),
						f"{student.average:.2f}",
						student.grade,
					)
				)
		return True
	except (OSError, csv.Error) as error:
		print(f"Unable to save student records: {error}")
		return False


def load_students(filename: str = "student_grades.txt") -> dict[str, Student]:
	"""Load student records, returning an empty collection if none exists."""
	students: dict[str, Student] = {}
	try:
		with open(filename, newline="", encoding="utf-8") as file:
			for row in csv.DictReader(file, delimiter="|"):
				student = Student(
					row["id"],
					row["name"],
					row["id"],
					row["name"],
					float(row["test1"]),
					float(row["test2"]),
					float(row["test3"]),
				)
				students[student.student_id] = student
	except FileNotFoundError:
		print("No existing student_grades.txt file found. Starting with no records.")
	except (OSError, csv.Error, KeyError, TypeError, ValueError) as error:
		print(f"Unable to load student records: {error}")
	return students


def print_menu() -> None:
	"""Display the available actions."""
	print("\nStudent Record Manager")
	print("1. Add student")
	print("2. Update test score")
	print("3. Find student")
	print("4. Display all students")
	print("5. Display class statistics")
	print("6. Remove student")
	print("Press ESC to save and exit.")


def main() -> None:
	"""Run the interactive student record manager."""
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s) from student_grades.txt.")
	actions = {
		"1": add_student,
		"2": update_score,
		"3": find_student,
		"4": show_all_students,
		"5": show_statistics,
		"6": remove_student,
	}

	while True:
		print_menu()
		choice = input("Choose an option or press ESC: ")
		if choice == "\x1b" or choice.strip().upper() == "ESC":
			if save_students(students):
				print("Student records saved to student_grades.txt. Goodbye!")
			else:
				print("The program is closing without saving changes.")
			break
		action = actions.get(choice)
		if action is None:
			print("Please choose an option from 1 through 6.")
		else:
			action(students)


if __name__ == "__main__":
	main()