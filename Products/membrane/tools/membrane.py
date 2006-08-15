from ZODB.PersistentMapping import PersistentMapping
from Globals import InitializeClass
from Acquisition import aq_base, aq_chain
from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from ComputedAttribute import ComputedAttribute

from zope.interface import implements
from zope.interface import providedBy
from zope.app.apidoc.component import getRequiredAdapters
from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.event import notify

from Products.ZCatalog.ZCatalog import ZCatalog

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.CatalogTool import CatalogTool as BaseTool
from Products.CMFPlone.CatalogTool import registerIndexableAttribute

from Products.membrane.interfaces import IMembraneTool
from Products.membrane.interfaces import IUserAuthentication
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IUserRelated
from Products.membrane.interfaces import IGroup

from Products.membrane import permissions
from Products.membrane.config import TOOLNAME
from Products.membrane.events import MembraneTypeRegisteredEvent
from Products.membrane.events import MembraneTypeUnregisteredEvent

# Use extensible object wrapper to always list the interfaces
def object_implements(object, portal, **kw):
    # XXX this is NOT very efficient  :-(
    def getDottedName(iface):
        # have to do this b/c z2->z3 bridges don't play well
        # w/ __identifier__
        return "%s.%s" % (iface.__module__, iface.__name__)
    
    res = {}
    for iface in providedBy(object).flattened():
        res[getDottedName(iface)] = iface
    direct = res.values()
    for iface in direct:
        for adapter_reg in getRequiredAdapters(iface):
            adaptable_iface = adapter_reg.provided
            adapting_from = [i for i in adapter_reg.required if i is not None]
            skip = False
            if len(adapting_from) > 1:
                # only support multiadapters that this object can satisfy alone
                for i in adapting_from:
                    if not i in direct:
                        skip = True
            if adaptable_iface is not None and not skip:
                res[getDottedName(adaptable_iface)] = adaptable_iface
    return res.keys()

registerIndexableAttribute('object_implements', object_implements)


def getUserName(object, portal, **kw):
    try:
        object = IUserAuthentication(object)
    except TypeError:
        return None
    return object.getUserName()

registerIndexableAttribute('getUserName', getUserName)


def getUserId(object, portal, **kw):
    try:
        object = IUserRelated(object)
    except TypeError:
        return None
    return object.getUserId()

registerIndexableAttribute('getUserId', getUserId)


def getGroupId(object, portal, **kw):
    try:
        object = IGroup(object)
    except TypeError:
        return None
    return object.getGroupId()

registerIndexableAttribute('getGroupId', getGroupId)


def getParentPath(object, portal, **kw):
    """
    Returns the physical path of the parent object.
    """
    return '/'.join(object.aq_parent.getPhysicalPath())

registerIndexableAttribute('parent_path', getParentPath)


class Record:
    """ A simple helper class for carrying the 'extra'-payload to
    index constructors.
    """
    def __init__(self, **kw):
        self.__dict__.update(kw)


class MembraneTool(BaseTool):
    """Tool for managing members."""
    id = TOOLNAME
    toolicon = 'tool.gif'

    meta_type = 'MembraneTool'
    archetype_name = 'MembraneTool'

    implements(IMembraneTool, IAttributeAnnotatable)

    manage_options=(
        {'label': 'Types', 'action': 'manage_membranetypes'},
        {'label': 'Status Map', 'action': 'manage_statusmap'},
        ) + BaseTool.manage_options

    security = ClassSecurityInfo()

    def __init__(self, *args, **kwargs):
        ZCatalog.__init__(self, self.getId())

    security.declareProtected(permissions.ManagePortal, 'registerMembraneType')
    def registerMembraneType(self, portal_type):
        attool = getToolByName(self, 'archetype_tool')
        catalogs = [x.getId() for x in attool.getCatalogsByType(portal_type)]
        if TOOLNAME not in catalogs:
            catalogs.append(TOOLNAME)
            attool.setCatalogsByType(portal_type, catalogs)
            notify(MembraneTypeRegisteredEvent(self, portal_type))

    security.declareProtected(permissions.ManagePortal, 'unregisterMembraneType')
    def unregisterMembraneType(self, portal_type):
        attool = getToolByName(self, 'archetype_tool')
        catalogs = [x.getId() for x in attool.getCatalogsByType(portal_type)]
        if TOOLNAME in catalogs:
            catalogs.remove(TOOLNAME)
            attool.setCatalogsByType(portal_type, catalogs)
            notify(MembraneTypeUnregisteredEvent(self, portal_type))

    security.declareProtected(permissions.VIEW_PUBLIC_PERMISSION,
                              'listMembraneTypes')
    def listMembraneTypes(self):
        mtypes = []
        attool = getToolByName(self, 'archetype_tool')
        catalog_map = getattr(aq_base(attool), 'catalog_map', {})
        for t,c in catalog_map.items():
            if self.getId() in c:
                mtypes.append(t)
        return mtypes

    security.declareProtected(permissions.VIEW_PUBLIC_PERMISSION,
                              'getUserAuthProvider')
    def getUserAuthProvider(self, login):
        """
        Return the unique object that is the authentication provider
        for the provided login.
        """
        uSR = self.unrestrictedSearchResults
        members = uSR(getUserName=login,
                      object_implements=IMembraneUserAuth.__identifier__)

        if not members:
            return None

        assert len(members) == 1
        member = members[0]._unrestrictedGetObject()
        return member

    def _createTextIndexes(self, item, container):
        """Create getUserName, getUserId, getGroupId text indexes."""

        self.manage_addProduct['ZCTextIndex'].manage_addLexicon(
            'lexicon',
            elements=[
            Record(group='Case Normalizer', name='Case Normalizer'),
            Record(group='Stop Words', name=" Don't remove stop words"),
            Record(group='Word Splitter', name="Unicode Whitespace splitter"),
            ])

        txt_idxs = ('Title', 'getUserName', 'getUserId', 'getGroupId')
        for index in txt_idxs:
            self.manage_addIndex(index,
                                 'ZCTextIndex',
                                 Record(lexicon_id='lexicon',
                                        index_type='Cosine Measure'))


InitializeClass(MembraneTool)
