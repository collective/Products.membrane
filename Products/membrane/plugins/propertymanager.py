# Copyright 2005 Plone Solutions
# info@plonesolutions.com

from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IReferenceable

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IPropertiesPlugin

from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin
from Products.PlonePAS.sheet import MutablePropertySheet
from Products.membrane.config import TOOLNAME
from Products.membrane.interfaces import IMembraneUserProperties

manage_addMembranePropertyManagerForm = PageTemplateFile(
    '../www/MembranePropertyManagerForm',
    globals(), __name__='manage_addMembranePropertyManagerForm' )

def addMembranePropertyManager( dispatcher, id, title=None, REQUEST=None ):
    """ Add a MembranePropertyManager to a Pluggable Auth Service. """

    pmm = MembranePropertyManager(id, title)
    dispatcher._setObject(pmm.getId(), pmm)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'MembranePropertyManager+added.'
                            % dispatcher.absolute_url())


class MembranePropertyManager(BasePlugin, Cacheable):
    """ PAS plugin for managing properties on contentish users and groups
        in Plone.
    """

    meta_type = 'Membrane Property Manager'

    security = ClassSecurityInfo()

    implements(IPropertiesPlugin, IMutablePropertiesPlugin)

    def __init__(self, id, title=None):

        self._id = self.id = id
        self.title = title

    def _getPropertyProviders(self, user):
        mbtool = getToolByName(self, TOOLNAME)
        ob_imp_query = {'query': (IMembraneUserProperties.__identifier__,
                                  IReferenceable.__identifier__),
                        'operator': 'and'}
        uSR = mbtool.unrestrictedSearchResults
        isGroup = getattr(user, 'isGroup', lambda:None)()
        if not isGroup:
            prop_providers = uSR(exact_getUserId=user.getId(),
                                 object_implements=ob_imp_query)
        else:
            prop_providers = uSR(exact_getGroupId=user.getId(),
                                 object_implements=ob_imp_query)
        for pp in prop_providers:
            yield pp._unrestrictedGetObject()

    #
    #   IMutablePropertiesPlugin implementation
    #   IPropertiesPlugin implementation
    #
    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        """
        Retrieve all the IMembraneUserProperties property providers
        and delegate to them.
        """
        properties = {}
        mbtool = getToolByName(self, TOOLNAME)
        # first get the auth provider to get the uid property
        member = mbtool.getUserAuthProvider(user.getUserName())
        if member is not None:
            # XXX do we want a 'uid' property for groups?
            properties['uid'] = IReferenceable(member).UID()

        prop_providers = self._getPropertyProviders(user)
        for pp in prop_providers:
            mem_props = IMembraneUserProperties(pp)
            psheet = mem_props.getPropertiesForUser(user, request)
            for prop, value in psheet.propertyItems():
                properties[prop] = value
        if properties.has_key('id'):
            # When instantiating sheet(id, **props) is used - two ids is bad
            del properties['id']
        return MutablePropertySheet(self.id,
                                    **properties)

    security.declarePrivate('setPropertiesForUser')
    def setPropertiesForUser(self, user, propertysheet):
        """
        Retrieve all of the IMembraneUserProperties property providers
        and delegate to them.
        """
        prop_providers = self._getPropertyProviders(user)
        for pp in prop_providers:
            mem_props = IMembraneUserProperties(pp)
            mem_props.setPropertiesForUser(user, propertysheet)
            
    security.declarePrivate('deleteUser')
    def deleteUser(self, user_id):
        """
        XXX: TODO
        """
        pass

InitializeClass(MembranePropertyManager)
