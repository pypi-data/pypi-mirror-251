import datetime
import math
import os
import pathlib
from typing import Callable

from todotree.Config.Config import Config
from todotree.Errors.ProjectFolderError import ProjectFolderError
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError
from todotree.Managers.AbstractManager import AbstractManager
from todotree.Task.ConsoleTask import ConsoleTask
from todotree.Task.Task import Task
from todotree.Tree import Tree


class TaskManager(AbstractManager):
    """Manages the tasks."""
    not_found_error = TodoFileNotFoundError

    @property
    def number_of_digits(self) -> int:
        """Property which defines the number of digits of the task in the task list with the highest number."""
        maxi = max([x.i for x in self.task_list])
        return int(math.ceil(math.log(maxi + 1, 10)))

    def __init__(self, configuration: Config):
        """Initializes a task manager, which manages the tasks."""

        super().__init__()
        self.task_list: list[Task] = []
        """List Without empty lines"""

        self.config: Config = configuration
        """Configuration settings for the application."""

        self.file = self.config.paths.todo_file
        """txt file location."""

    # Imports

    def import_tasks(self):
        """
        Import the tasks and projects from files.
        """
        super().import_tasks()
        if self.config.enable_project_folder:
            self._import_project_folder()

    def filter_t_date(self):
        """Removes Tasks from the Taskmanager where the t:date is later than today."""
        self.task_list = [t for t in self.task_list if t.t_date is None or t.t_date <= datetime.date.today()]

    def filter_block(self):
        """
        Removes Tasks from the Taskmanager where the task is blocked by some other task.
        """
        # Detect all block items.
        block_list_items = [y for x in self.task_list for y in x.blocks]
        # Blocked / Blocked by filtering
        for task in self.task_list.copy():
            # Check if there is a task which is blocked by another task.
            if any(filter(lambda x: x in block_list_items, task.blocked)):
                self.task_list.remove(task)

    def _import_project_folder(self):
        """
        Adds the directory to the project tree.
        """
        try:
            for i in pathlib.Path(self.config.paths.project_tree_folder).glob("*/"):
                proj = os.path.basename(i)
                # Check if there is a task with that project.
                if not any(proj in x.projects for x in self.task_list):
                    tmp_task = Task(-1, self.config.emptyProjectString)
                    tmp_task.projects = [proj]
                    self.task_list.append(tmp_task)
        except FileNotFoundError as e:
            raise ProjectFolderError(f"An error occurred while processing the projects folder: {e}")

    def print_tree(self, key):
        """Prints a tree representation of the task list.
        :key: The key of the task used for the first line."""
        self.filter_t_date()
        self.filter_block()
        tasks = [ConsoleTask(task.i, task.task_string, total_digits=self.number_of_digits) for task in self.task_list]

        print_function: Callable[[str, ConsoleTask], str]
        match key:
            case "projects":
                def print_function(project_to_exclude, task):
                    return task.print_project(project_to_exclude)
                root_name = "Projects"
                empty_string = self.config.noProjectString
            case "contexts":
                def print_function(context_to_exclude, task):
                    return task.print_context(context_to_exclude)
                root_name = "Contexts"
                empty_string = self.config.noContextString
            case "due":
                def print_function(_, task):
                    return task.print_due()
                root_name = "Due Dates"
                key = "due_date_band"
                empty_string = "default"
            case _:
                raise NotImplementedError(key)
        return str(Tree(tasks, key, treeprint=self.config.tree_print,
                        print_func=print_function, root_name=root_name, empty_string=empty_string))

    def add_or_update_task(self, task_number, func: Callable, *args, **kwargs) -> Task:
        """
        Runs `func` on the task with `task_number`.
        :param task_number: The task number.
        :param func: The Task function.
        :param args: passed to func.
        :param kwargs: passed to func.
        :return: The updated task.
        """
        func(self.task_list[task_number - 1], *args, **kwargs)
        self.write_to_file()
        return self.task_list[task_number - 1]

    def append_to_task(self, task_number: int, task_string: str) -> Task:
        """
        Appends `task_string` to the task defined by `task_number`.
        :param task_string: The string to append
        :param task_number: The number of the existing task.
        :return: The new merged task.
        """
        self.task_list[task_number - 1] = self.task_list[task_number - 1] + task_string
        self.write_to_file()
        return self.task_list[task_number - 1]

    def __str__(self, filter_string=None):
        """
        Filters the task list by whether `filter_string` occurred in the task.
        """
        # Prepare the lists.
        self.filter_t_date()
        self.filter_block()
        if filter_string:
            self.task_list = [item for item in self.task_list if filter_string in item.task_string]
        self.task_list.sort(key=lambda x: x.priority)
        # Output the list.
        return super().__str__()
