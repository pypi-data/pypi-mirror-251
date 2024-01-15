from collections import defaultdict
from typing import Callable

from todotree.Config.TreePrint import TreePrint
from todotree.Task.Task import Task


class Tree:
    """
    Class representing a tree.

    The tree is a graph structure where there are no loops.
    However, this one is a special version of it.
    This tree is only 2 nodes deep.
    The leaves are the actual objects.
    The first layer of nodes consist of the value of one of the attributes of the leaves.
    Leaves with the same attribute are connected to the same node.

    To print the tree, simply cast it to string, like so `str(Tree())`.
    """

    def __init__(self, list_to_convert, key, **kwargs):
        """
        :param list_to_convert: the list to convert to a tree.
        :param key: the key of the first node in the tree.

        :param Optional arguments:
          - root_name: The display name of the root node.
          - empty_string: The display name of the "empty" or "default" first node.
          - config: The configuration file for printing the tree.
        """

        self.data_structure: defaultdict[str, list[Task]] = defaultdict(list)
        """
        The data structure of this tree.
        """

        self.root_name: str = kwargs.pop("root_name", "root")
        """
        The name of the root of the tree.
        """

        self.empty_string: str = kwargs.pop("empty_string", "default")
        """
        The 'empty' category.
        """

        self.treeprint: TreePrint = kwargs.pop('treeprint', TreePrint("t", "l", "s", "e"))
        """
        The application configuration.
        """

        self.print_func: Callable[[str, Task], str] = kwargs.pop('print_func', lambda key_value, task: str(task))
        """
        Function which prints the task.
        Input are: key_value: The value of the key given by `key`.
        Output must be a string.
        """

        # Generate tree.
        self.generate_tree(list_to_convert, key)

    def generate_tree(self, list_to_parse: list, key: str):
        """
        Generate a tree like dictionary from the task list.
        The first line is each distinct key.
        Which points to a list of tasks. Tasks can appear in multiple lists.

        :list list_to_parse: The list to parse.
        :key: The key to index to, such as due:date, project or context.
        """
        for task in list_to_parse:
            if isinstance(getattr(task, key), list) and len(getattr(task, key)) > 0:
                for key_value in getattr(task, key):
                    self.data_structure[key_value].append(task)
            else:
                # It is a single item.
                self.data_structure[getattr(task, key) if getattr(task, key) else self.empty_string].append(task)

    def __str__(self):
        """
        Used for pretty printing the tree.
        """
        # Edge case: empty list -> empty string.
        if self.data_structure == {}:
            return ""

        return self.__outer_loop(self.root_name + "\n")

    def __outer_loop(self, return_string):
        """Construct the string over the dict."""
        for i, first_node in enumerate(self.data_structure.keys()):
            # Print the outer node. This prints the value of the key.
            return_string += self.treeprint.t_print if (i < len(self.data_structure) - 1) else self.treeprint.s_print
            # Section with the name of the first node.
            return_string += first_node + "\n"
            # Inner loop.
            return_string = self.__inner_loop(self.data_structure[first_node], first_node, i, len(self.data_structure), return_string)
        return return_string

    def __inner_loop(self, first_list, first_node, i, len_first_node, return_string):
        """Construct the string over the list."""
        for j, second_node in enumerate(first_list):
            return_string += (
                    (self.treeprint.l_print if (i < len_first_node - 1) else self.treeprint.e_print)  # First prefix.
                    + (self.treeprint.t_print if (j < len(first_list) - 1) else self.treeprint.s_print)  # 2nd prefix.
                    + self.print_func(first_node, second_node) + "\n")  # Actual task.
        return return_string
