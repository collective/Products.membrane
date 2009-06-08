from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane.utils import getAllWFStatesForType

def doInitializeStatusCategories(tool, portal_type):
    """
    Perform the initialization
    """
    cat_map = ICategoryMapper(tool)
    cat_set = generateCategorySetIdForType(portal_type)
    cat_map.addCategorySet(cat_set)
    cat_map.addCategory(cat_set, ACTIVE_STATUS_CATEGORY)

    states = getAllWFStatesForType(tool, portal_type)
    for state in states:
        cat_map.addToCategory(cat_set, ACTIVE_STATUS_CATEGORY,
                              state)

def initializeStatusCategories(event):
    """
    Initializes the category sets and categories of a category mapper
    to be used to track "active" workflow states for a membrane type.
    Triggered when a new membrane type is registered.  Defaults to all
    workflow states being active.
    """
    doInitializeStatusCategories(event.tool, event.portal_type)

def removeStatusCategories(event):
    """
    Removes the related status categories from the category mapper
    when a membrane type is unregistered.
    """
    cat_map = ICategoryMapper(event.tool)
    cat_set = generateCategorySetIdForType(event.portal_type)
    cat_map.delCategorySet(cat_set)
