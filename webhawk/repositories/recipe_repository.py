import os
from operator import itemgetter

from lib import common

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Dimi Balaouras - Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class FileRecipeRepository(object):
    """
    Retrieves and Build Recipes from files
    """

    name = "recipe_repository"

    def __init__(self, context):
        """
        Class initialisation
        """
        self._context = context
        self._logger = context.get("logger")
        self._recipes_file = context["config"]["recipes_file_path"]

        self._logger.info("Attempting to load Recipes from file '%s'" % self._recipes_file)

        # Load Recipes
        if not os.path.isfile(self._recipes_file):
            raise EnvironmentError("Recipes file '%s' does not exist in '%s'" % (self._recipes_file, os.getcwd()))
        self._recipes = common.load_config(self._recipes_file)

        # Store recipe id inside the recipe
        for recipe_id in self._recipes:
            self._recipes[recipe_id]['id'] = recipe_id

        self._logger.info("Loaded %s recipes" % len(self._recipes))

    def find_one(self, id):
        """
        Get recipe by id
        :param id: The id of the recipe
        :return: The Recipe object if found; None otherwise
        """
        return self._recipes.get(id, None)

    def find_by_name_and_branch(self, name, branch):
        """
        Get recipe by name and branch
        :param name: Repository Name
        :param branch: Branch of the repository
        :return: The Recipe object if found; None otherwise
        """
        recipe = None
        self._logger.debug("Searching for %s/%s in %s" % (name, branch, self._recipes))
        try:
            for recipe_id in self._recipes:
                recipe_cand = self._recipes[recipe_id]
                if recipe_cand['repository']['name'] == name and recipe_cand['repository']['branch'] == branch:
                    recipe = recipe_cand
                    recipe['id'] = recipe_id
                    break
        except Exception:
            # Recipe not found
            pass

        return recipe

    def find_by_name_and_star_wildcard(self, name):
        """
        Get recipe by name and star (asterisk) wildcard
        :param name: Repository Name
        :return: The Recipe object if found; None otherwise
        """
        # Basically, do same thing as find_by_name_and_branch does..but look for an asterisk instead of specific branch
        return self.find_by_name_and_branch(name=name, branch="*")

    def find_all(self):
        """
        Get all recipes
        :return: The Recipe objects in a list
        """
        return sorted([self._format_recipe(name, self._recipes[name]) for name in self._recipes], key=itemgetter("id"))

    def count(self, query=None):
        """
        Counts the number of Resources entities
        :param query: A query parameter (not used in this implementation)
        :return: The number of Recipy objects found in the file
        """
        return len(self._recipes)

    def _format_recipe(self, name, recipe):
        """
        Format the recipe

        :param recipe:
        :return:
        """
        recipe["id"] = name
        return recipe
