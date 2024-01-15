import math
import shutil
from abc import ABC
from pathlib import Path
# https://docs.python.org/3/library/tempfile.html
from tempfile import NamedTemporaryFile

from todotree.Errors.NoSuchTaskError import NoSuchTaskError
from todotree.Task.ConsoleTask import ConsoleTask
from todotree.Task.Task import Task


class AbstractManager(ABC):
    not_found_error = FileNotFoundError
    """Error to raise when the database file is not found."""
    
    @property
    def number_of_digits(self) -> int:
        """Property which defines the number of digits of the task in the task list with the highest number."""
        maxi = max([x.i for x in self.task_list])
        return int(math.ceil(math.log(maxi + 1, 10)))

    def __init__(self):
        self.file: Path = Path("/")
        """Path to the 'database' file. Must be set in the subclass."""

        self.task_list: list[Task] = []
        """Task list"""

    def remove_task_from_file(self, task_number: int) -> Task:
        # Remove task.
        try:
            removed_task = self.task_list.pop(task_number - 1)
        except IndexError as e:
            raise NoSuchTaskError(f"Task {task_number} does not exist in {self.file.name}.") from e
        self.write_to_file()
        return removed_task

    def remove_tasks_from_file(self, task_numbers: list[int]) -> list[Task]:
        removed_tasks = []
        task_numbers.sort()
        task_numbers.reverse()
        for task_number in task_numbers:
            try:
                removed_tasks.append(self.task_list.pop(task_number - 1))
            except IndexError as e:
                raise NoSuchTaskError(f"Task {task_number} does not exist in {self.file}.") from e
        self.write_to_file()
        return removed_tasks

    def write_to_file(self):
        """Writes the entire list to the file."""
        # Sort task list.
        self.task_list.sort(key=lambda x: x.i)
        #  Delete=false is needed for windows, I hope that somebodies temp folder won't be clobbered with this...
        try:
            with NamedTemporaryFile("w+t", newline="", delete=False) as temp_file:
                # may strip new lines by using task list.
                for task in self.task_list:
                    temp_file.write(task.to_file())
                temp_file.flush()
                shutil.copy(temp_file.name, self.file)
        except FileNotFoundError as e:
            raise self.not_found_error from e

    def add_tasks_to_file(self, tasks: list[Task]) -> list[Task]:
        """Append multiple tasks to the file."""
        try:
            maxi = max([task.i for task in self.task_list]) + 1
        except ValueError:
            # The list is empty.
            maxi = 0
        try:
            with self.file.open(mode="a") as f:
                for i, task in enumerate(tasks):
                    f.write(task.to_file())
                    task.i = maxi + i
        except FileNotFoundError as e:
            raise self.not_found_error from e
        return tasks

    def import_tasks(self):
        """Imports the tasks from the database file."""
        try:
            with self.file.open('r') as f:
                content = f.readlines()
                for i, task in enumerate(content):
                    # Skip empty lines.
                    if task.strip() == "":
                        continue
                    self.task_list.append(Task(i + 1, task.strip()))
        except FileNotFoundError as e:
            raise self.not_found_error() from e

    def __str__(self):
        """List the tasks."""
        s = ""
        for tsk in [ConsoleTask(task.i, task.task_string, self.number_of_digits) for task in self.task_list]:
            s += str(tsk) + "\n"
        return s

