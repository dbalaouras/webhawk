import os
import sys

__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/../webhawk" % __abs_dirpath__)

from nose.tools import assert_is_not_none, assert_is_none, assert_is_instance, assert_equal
from lib.common import get_logger
from repositories.recipe_repository import FileRecipeRepository
from services.app_context import AppContext

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Dimi Balaouras - Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."

# Prepare the Guinea Pig
logger = get_logger({}, "recipe_repository_test")
config = {
    "recipes_file_path": "%s/%s" % (__abs_dirpath__, "mock-recipes.yaml")
}
context = AppContext(allow_replace=False)
context.register("config", config)
context.register("logger", logger)

recipe_repository = FileRecipeRepository(context=context)


def test_find_by_name_and_branch():
    """
    Test if the recipe file repository can find a recipe by name and repository
    """
    recipe = recipe_repository.find_by_name_and_branch("myapp", "develop")
    assert_is_not_none(recipe)
    assert_is_instance(obj=recipe, cls=dict)

    recipe = recipe_repository.find_by_name_and_branch("myapp-fake", "develop")
    assert_is_none(recipe)


def test_find_by_id():
    """
    Test if the recipe file repository can find a recipe by id
    """
    recipe = recipe_repository.find_one(id="myapp-develop")
    assert_is_not_none(recipe)
    assert_is_instance(obj=recipe, cls=dict)

    recipe = recipe_repository.find_one(id="myapp-develop-fake")
    assert_is_none(recipe)


def test_find_all():
    """
    Test if the recipe file repository can find a recipe by id
    """
    recipes = recipe_repository.find_all()
    assert_is_not_none(recipes)
    assert_is_instance(obj=recipes, cls=list)
    assert_equal(len(recipes), 2)
