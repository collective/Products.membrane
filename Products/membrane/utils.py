from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from config import STATUS_CATEGORY_SET
from config import FILTERED_ROLES
from config import TOOLNAME
from interfaces import IUserAdder

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

def getCurrentUserAdder(context):
    """
    Returns the appropriate IUserAdder utility, or None if it can't be
    retrieved.
    """
    portal = getToolByName(context, 'portal_url').getPortalObject()
    mbtool = getToolByName(context, TOOLNAME)

    sm = portal.getSiteManager()

    adder_name = mbtool.user_adder
    if adder_name:
        # will be None if it can't be found
        adder = sm.queryUtility(IUserAdder, name=adder_name)
    else:
        adders = sm.getUtilitiesFor(IUserAdder)
        try:
            name, adder = adders.next()
        except StopIteration:
            adder = None

    return aq_base(adder).__of__(context)

def queryMembraneTool(context, **query):
    mbtool = getToolByName(context, TOOLNAME)
    uSR = mbtool.unrestrictedSearchResults
    return uSR(**query)

def findImplementations(context, iname):
    return queryMembraneTool(context, 
                             object_implements=iname.__identifier__)

# convenience cache key for use in adapters (i.e. views) and tools
def membraneCacheKey(method, self, *args, **kw):
    mbtool = getToolByName(self.context, TOOLNAME)
    return '/'.join(mbtool.getPhysicalPath()), mbtool.getCounter()

