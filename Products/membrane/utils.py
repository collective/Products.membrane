from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from config import FILTERED_ROLES
from config import TOOLNAME
from interfaces import IUserAdder


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

    if adder is not None:
        adder = aq_base(adder).__of__(context)
    return adder


def findMembraneUserAspect(context, iface, **query):
    """Return all instances of a *membrane aspect* for objects matching
    the given catalog query.

    To get the content objects instead of the interface implementation
    use :py:func:`findImplementations` instead.
    """
    return filter(None,
        [iface(brain._unrestrictedGetObject(), None)
        for brain in findImplementations(context, iface, **query)])


def findImplementations(context, iface, **query):
    """Return a list of all objects that can provide, either directly or via
    an adapter, a given membrane interface. This requires that the interfaces
    have :py:obj:`IMembraneQueryableInterface` providing utilities. This is
    true for all standard membrane interfaces.

    Use :py:func:`findMembraneUserAspect` if you want to get the object that
    implements the interface (which can be an adapter).
    """
    return getToolByName(
        context, TOOLNAME).unrestrictedSearchResults(
            object_implements=iface.__identifier__, **query)


# convenience cache key for use in adapters (i.e. views) and tools
def membraneCacheKey(method, self, *args, **kw):
    mbtool = getToolByName(self.context, TOOLNAME)
    return '/'.join(mbtool.getPhysicalPath()), mbtool.getCounter()
