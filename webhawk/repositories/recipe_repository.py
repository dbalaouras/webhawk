import os

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

        # Load Recipes
        self._recipes_file = context["config"]["recipes_file_path"]
        if not os.path.isfile(self._recipes_file):
            raise EnvironmentError("Recipes file '%s' does not exist in '%s'" % (self._recipes_file, os.getcwd()))
        self._recipes = common.load_config(self._recipes_file)
        self._logger = context.get("logger")
        self._context = context

        self._logger.info("Loading Recipes from file '%s'" % self._recipes_file)

    def find_one(self, id):
        """
        Get recipe by id
        :param id: The id of the recipe
        :return: The Recipe object if found; None otherwise
        """
        return self._recipes.get(id, None)

    def find_by_name_and_branch(self, name, branch):
        """
        Get recipe by name
        :param name: Repository Name
        :param branch: Branch of the repository
        :return: The Recipe object if found; None otherwise
        """
        recipe = None
        self._logger.debug("Searching for %s/%s in %s" % (name, branch, self._recipes))
        for recipe_name in self._recipes:
            recipe_cand = self._recipes[recipe_name]
            if recipe_cand['repository']['name'] == name and recipe_cand['repository']['branch'] == branch:
                recipe = recipe_cand
                break

        return recipe

    def find_all(self):
        """
        Get all recipes
        :return: The Recipe objects in a list
        """
        return [self._format_recipe(name, self._recipes[name]) for name in self._recipes]

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
