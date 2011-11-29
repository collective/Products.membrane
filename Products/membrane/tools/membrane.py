from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.event import notify

from App.class_init import InitializeClass
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from persistent.list import PersistentList

from Products.ZCatalog.ZCatalog import ZCatalog

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal

from Products.CMFPlone.CatalogTool import CatalogTool as BaseTool

from Products.membrane.interfaces.membrane_tool import IMembraneTool
from Products.membrane.interfaces import user as user_ifaces

from Products.membrane import permissions
from Products.membrane.config import TOOLNAME
from Products.membrane.config import USE_COLLECTIVE_INDEXING
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

    manage_options = (
        {'label': 'Types', 'action': 'manage_membranetypes'},
        {'label': 'Status Map', 'action': 'manage_statusmap'},
        ) + BaseTool.manage_options

    security = ClassSecurityInfo()

    def __init__(self, *args, **kwargs):
        ZCatalog.__init__(self, self.getId())
        self.membrane_types = PersistentList()

    def registerMembraneType(self, portal_type):
        if not USE_COLLECTIVE_INDEXING:
            attool = getToolByName(self, 'archetype_tool')
            catalogs = [x.getId() for x in
                        attool.getCatalogsByType(portal_type)]
            if TOOLNAME not in catalogs:
                catalogs.append(TOOLNAME)
                attool.setCatalogsByType(portal_type, catalogs)
        elif portal_type not in self.membrane_types:
            self.membrane_types.append(portal_type)

        # Trigger the status maps even if the type is already registered.
        notify(MembraneTypeRegisteredEvent(self, portal_type))
    security.declareProtected(ManagePortal, 'registerMembraneType')

    def unregisterMembraneType(self, portal_type):
        if not USE_COLLECTIVE_INDEXING:
            attool = getToolByName(self, 'archetype_tool')
            catalogs = [x.getId() for x in
                        attool.getCatalogsByType(portal_type)]
            if TOOLNAME in catalogs:
                catalogs.remove(TOOLNAME)
                attool.setCatalogsByType(portal_type, catalogs)
        elif portal_type in self.membrane_types:
            self.membrane_types.remove(portal_type)
            notify(MembraneTypeUnregisteredEvent(self, portal_type))
    security.declareProtected(ManagePortal, 'unregisterMembraneType')

    def listMembraneTypes(self):
        if not USE_COLLECTIVE_INDEXING:
            mtypes = []
            attool = getToolByName(self, 'archetype_tool')
            catalog_map = getattr(aq_base(attool), 'catalog_map', {})
            for t, c in catalog_map.items():
                if self.getId() in c:
                    mtypes.append(t)
            return mtypes
        else:
            return self.membrane_types
    security.declareProtected(permissions.VIEW_PUBLIC_PERMISSION,
                              'listMembraneTypes')

    def getUserObject(self, login=None, user_id=None, brain=False):
        """
        Return the authentication implementation for a given login or userid.
        """
        query = {}
        if user_id:
            if self.case_sensitive_auth and \
                   ('exact_getUserId' in self._catalog.indexes):
                query["exact_getUserId"] = user_id
            else:
                query["getUserId"] = user_id
        elif login:
            if self.case_sensitive_auth and \
                   ('exact_getUserName' in self._catalog.indexes):
                query["exact_getUserName"] = login
            else:
                query["getUserName"] = login

        if not query:  # No user_id or login name given
            return None

        query["object_implements"
              ] = user_ifaces.IMembraneUserAuth.__identifier__
        uSR = self.unrestrictedSearchResults
        members = uSR(**query)

        # filter out inadvertent ZCTextIndex matches by only keeping
        # records with the same number of characters
        if "getUserName" in query:
            members = [mem for mem in members
                       if len(mem.getUserName) == len(login)]
        if "getUserId" in query:
            members = [mem for mem in members
                       if len(mem.getUserId) == len(user_id)]

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
            bogus = [b.getPath() for b in members
                     if site_path not in b.getPath()]
            if len(bogus) == 1:
                # yup, clear it out and move on
                self._catalog.uncatalogObject(bogus[0])
                members = uSR(**query)

        assert len(members) == 1, (
            'more than one member found for "%s"'
            % (login or user_id))
        if brain:
            return members[0]

        member = members[0]._unrestrictedGetObject()
        return member
    security.declarePrivate('getUserObject')

    def getOriginalUserIdCase(self, userid):
        """
        Used to get the original case spelling of a given user id.
        """
        if userid == '':
            return None
        uSR = self.unrestrictedSearchResults
        query = {'getUserId': userid,
                 'object_implements':
                 user_ifaces.IMembraneUserAuth.__identifier__}
        members = uSR(**query)
        # filter out inadvertent ZCTextIndex matches by only keeping
        # records with the same number of characters
        members = [mem for mem in members
                   if len(mem.getUserId) == len(userid)]

        if not members:
            return None

        assert len(members) == 1
        return members[0].getUserId


InitializeClass(MembraneTool)
