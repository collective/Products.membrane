import warnings

warnings.warn(
    'Products.membrane - The CategoryMapper support will be removed '
    'in version 1.2', DeprecationWarning)

from zope.interface import Interface

class ICategoryMapper(Interface):
    """
    Allows arbitrary mapping of data points into categories.
    """
    def addCategorySet(category_set_id):
        """
        Add a category grouping.
        """

    def delCategorySet(category_set_id):
        """
        Destructively remove a category grouping.
        """

    def hasCategorySet(category_set_id):
        """
        Returns True or False depending on whether or not the category set
        exists.
        """

    def listCategorySets():
        """
        Returns the existing category set ids.
        """

    def addCategory(category_set_id, category_id):
        """
        Add a new category to the specified category set.
        """

    def delCategory(category_set_id, category_id):
        """
        Destructively remove a category from the specified category set.
        """

    def hasCategory(category_set_id, category_id):
        """
        Returns True or False depending on whether or not the category
        exists.
        """

    def listCategories(category_set_id):
        """
        Returns the id for each category in the specified category set.
        """

    def addToCategory(category_set_id, category_id, datum):
        """
        Adds the data point to the specified category.
        """

    def removeFromCategory(category_set_id, category_id, datum):
        """
        Removes the data point from the specified category, if it is in
        the category.
        """

    def replaceCategoryValues(category_set_id, category_id, data):
        """
        Destructively replaces all of the category values in the category
        with the passed in data.

        o data: a sequence of data points, must be iterable
        """

    def listCategoryValues(category_set_id, category_id):
        """
        Returns all of the data points in the specified category.
        """

    def isInCategory(category_set_id, category_id, datum):
        """
        Returns True if the data point is in the specified category,
        False otherwise.
        """
