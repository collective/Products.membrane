from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

def initializeStatusCategories(event):
    """
    Initializes the category sets and categories of a category mapper
    to be used to track "active" workflow states for a membrane type.
    Triggered when a new membrane type is registered.  Defaults to all
    workflow states being active.
    """
    cat_map = ICategoryMapper(event.tool)
    cat_set = generateCategorySetIdForType(event.portal_type)
    cat_map.addCategorySet(cat_set)
    cat_map.addCategory(cat_set, ACTIVE_STATUS_CATEGORY)

    wftool = getToolByName(event.tool, 'portal_workflow')
    chain = wftool.getChainForPortalType(event.portal_type)
    for wfid in chain:
        wf = getattr(wftool, wfid)
        states = wf.states.objectIds()
        for state in states:
            cat_map.addToCategory(cat_set, ACTIVE_STATUS_CATEGORY,
                                  state)

def removeStatusCategories(event):
    """
    Removes the related status categories from the category mapper
    when a membrane type is unregistered.
    """
    cat_map = ICategoryMapper(event.tool)
    cat_set = generateCategorySetIdForType(event.portal_type)
    cat_map.delCategorySet(cat_set)
