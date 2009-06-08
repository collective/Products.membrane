from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.event import notify

from Globals import InitializeClass
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo

from Products.ZCatalog.ZCatalog import ZCatalog

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal

from Products.CMFPlone.CatalogTool import CatalogTool as BaseTool

from Products.membrane.interfaces import IMembraneTool
from Products.membrane.interfaces import IMembraneUserAuth

from Products.membrane import permissions
from Products.membrane.config import TOOLNAME
from Products.membrane.events import MembraneTypeRegisteredEvent
from Products.membrane.events import MembraneTypeUnregisteredEvent


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

    user_adder = ''
    case_sensitive_auth = True

    _catalog_count = None

    implements(IMembraneTool, IAttributeAnnotatable)

    manage_options=(
        {'label': 'Types', 'action': 'manage_membranetypes'},
        {'label': 'Status Map', 'action': 'manage_statusmap'},
        ) + BaseTool.manage_options

    security = ClassSecurityInfo()

    def __init__(self, *args, **kwargs):
        ZCatalog.__init__(self, self.getId())

    security.declareProtected(ManagePortal, 'registerMembraneType')
    def registerMembraneType(self, portal_type):
        attool = getToolByName(self, 'archetype_tool')
        catalogs = [x.getId() for x in attool.getCatalogsByType(portal_type)]
        if TOOLNAME not in catalogs:
            catalogs.append(TOOLNAME)
            attool.setCatalogsByType(portal_type, catalogs)
        # Triger the status maps even if the type is already listed
        # with the archetypes tool
        notify(MembraneTypeRegisteredEvent(self, portal_type))

    security.declareProtected(ManagePortal, 'unregisterMembraneType')
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
    def getUserAuthProvider(self, login, brain=False):
        """
        Return the unique object that is the authentication provider
        for the provided login.
        """
        if not login: # could be either '' or None
            return None
        uSR = self.unrestrictedSearchResults
        idxname = 'getUserName'
        if self.case_sensitive_auth and \
               ('exact_getUserName' in self._catalog.indexes):
            idxname = 'exact_getUserName'
        query = {idxname: login,
                 'object_implements': IMembraneUserAuth.__identifier__}
        members = uSR(**query)
        # filter out inadvertent ZCTextIndex matches by only keeping
        # records with the same number of characters
        if idxname == 'getUserName':
            members = [mem for mem in members
                       if len(mem.getUserName) == len(login)]

        if not members:
            return None

        if len(members) == 2:
            # Usually this is an error case, but when importing or
            # pasting a copy of a Plone site, the catalog can have
            # duplicate entries.  If there are exactly 2 entries, and
            # one has a path that is not inside this Plone site, then
            # we assume this is what's happened and we clear out the
            # bogus entry.
            site = getToolByName(self, 'portal_url').getPortalObject()
            site_path = '/'.join(site.getPhysicalPath())
            bogus = [b.getPath() for b in members if site_path not in b.getPath()]
            if len(bogus) == 1:
                # yup, clear it out and move on
                self._catalog.uncatalogObject(bogus[0])
                members = uSR(**query)
        
        assert len(members) == 1, 'more than one member found for login "%s"' % login
        if brain:
            return members[0]

        member = members[0]._unrestrictedGetObject()
        return member

    def getOriginalUserIdCase(self, userid):
        """
        Used to get the original case spelling of a given user id.
        """
        if userid == '':
            return None
        uSR = self.unrestrictedSearchResults
        query = {'getUserId': userid,
                 'object_implements': IMembraneUserAuth.__identifier__}
        members = uSR(**query)
        # filter out inadvertent ZCTextIndex matches by only keeping
        # records with the same number of characters
        members = [mem for mem in members
                   if len(mem.getUserId) == len(userid)]

        if not members:
            return None

        assert len(members) == 1
        return members[0].getUserId
        

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
