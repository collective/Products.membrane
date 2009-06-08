from AccessControl import ClassSecurityInfo
from persistent.mapping import PersistentMapping
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import CATEGORY_ANNOTATIONS_KEY

class CategoryMapper(object):
    """
    Adapts from IAnnotatable to ICategoryMapper, provides a mechanism
    for recording and retrieving "categories" of specific data points.
    Used by membrane to record the set of "active" workflow states.
    """
    security = ClassSecurityInfo()

    implements(ICategoryMapper)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if not annotations.has_key(CATEGORY_ANNOTATIONS_KEY):
            annotations[CATEGORY_ANNOTATIONS_KEY] = PersistentMapping()
        self.storage = annotations[CATEGORY_ANNOTATIONS_KEY]

    def _getCatSet(self, category_set_id):
        """
        Encapsulates retrieving category set and raising the appropriate
        exception if it isn't found.
        """
        cat_set = self.storage.get(category_set_id)
        if cat_set is None:
            raise KeyError, "Category set '%s' does not exist" % category_set_id
        return cat_set

    def _getCategory(self, category_set_id, category_id):
        """
        Encapsulates retrieving a specific category, raising the appropriate
        exception if either category set or category aren't found.
        """
        cat_set = self._getCatSet(category_set_id)
        category = cat_set.get(category_id)
        if category is None:
            raise KeyError, "Category '%s' does not exist" % category_id
        return category

    #
    # ICategoryMapper implementation
    #
    def addCategorySet(self, category_set_id):
        if not self.storage.has_key(category_set_id):
            self.storage[category_set_id] = PersistentMapping()
            self.context._p_changed = True

    def delCategorySet(self, category_set_id):
        self.storage.pop(category_set_id, None)

    def hasCategorySet(self, category_set_id):
        return self.storage.has_key(category_set_id)

    def listCategorySets(self):
        return self.storage.keys()

    def addCategory(self, category_set_id, category_id):
        cat_set = self._getCatSet(category_set_id)
        if not cat_set.has_key(category_id):
            cat_set[category_id] = PersistentMapping()

    def delCategory(self, category_set_id, category_id):
        cat_set = self._getCatSet(category_set_id)
        cat_set.pop(category_id, None)

    def hasCategory(self, category_set_id, category_id):
        cat_set = self._getCatSet(category_set_id)
        return cat_set.has_key(category_id)

    def listCategories(self, category_set_id):
        cat_set = self._getCatSet(category_set_id)
        return cat_set.keys()

    def addToCategory(self, category_set_id, category_id, datum):
        category = self._getCategory(category_set_id, category_id)
        category.update({datum:1})

    def removeFromCategory(self, category_set_id, category_id, datum):
        category = self._getCategory(category_set_id, category_id)
        category.pop(datum, None)

    def replaceCategoryValues(self, category_set_id, category_id, data):
        cat_set = self._getCatSet(category_set_id)
        category = cat_set[category_id] = PersistentMapping()
        for datum in data:
            category.update({datum: 1})

    def listCategoryValues(self, category_set_id, category_id):
        category = self._getCategory(category_set_id, category_id)
        return category.keys()

    def isInCategory(self, category_set_id, category_id, datum):
        category = self._getCategory(category_set_id, category_id)
        return category.has_key(datum)
