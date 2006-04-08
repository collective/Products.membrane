from Products.CMFCore.utils import getToolByName
from config import STATUS_CATEGORY_SET
from config import FILTERED_ROLES

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

def getFilteredValidRolesForPortal(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    roles = dict.fromkeys(portal.validRoles())
    for filtered_role in FILTERED_ROLES:
        roles.pop(filtered_role, None)
    return roles.keys()

