from Products.CMFCore.utils import getToolByName
from config import STATUS_CATEGORY_SET

def generateCategorySetIdForType(portal_type):
    return "_".join((portal_type, STATUS_CATEGORY_SET))

def getAllWFStatesForType(context, portal_type):
    wftool = getToolByName(context, 'portal_workflow')
    chain = wftool.getChainForPortalType(portal_type)
    states = []
    for wfid in chain:
        wf = getattr(wftool, wfid)
        states += wf.states.objectIds()
    return states
