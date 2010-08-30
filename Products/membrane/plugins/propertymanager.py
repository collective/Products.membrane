# Copyright 2005 Plone Solutions
# info@plonesolutions.com

from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zope.interface import implements

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.propertysheets \
    import IPropertySheet

from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin
from Products.PlonePAS.sheet import MutablePropertySheet
from Products.membrane.interfaces import user as user_ifaces
from Products.membrane.utils import findMembraneUserAspect

manage_addMembranePropertyManagerForm = PageTemplateFile(
    '../www/MembranePropertyManagerForm',
    globals(), __name__='manage_addMembranePropertyManagerForm' )


def addMembranePropertyManager(dispatcher, id, title=None, REQUEST=None):
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
        isGroup = getattr(user, 'isGroup', lambda: None)()
        if not isGroup:
            query = dict(exact_getUserId=user.getId())
        else:
            query = dict(exact_getGroupId=user.getId())

        for pp in findMembraneUserAspect(
            self, user_ifaces.IMembraneUserProperties, **query):
            yield pp

    #
    #   IMutablePropertiesPlugin implementation
    #   IPropertiesPlugin implementation
    #
    def getPropertiesForUser(self, user, request=None):
        """
        Retrieve all the IMembraneUserProperties property providers
        and delegate to them.
        """
        properties = {}

        prop_providers = self._getPropertyProviders(user)
        for mem_props in prop_providers:
            psheet = mem_props.getPropertiesForUser(user, request)
            if psheet:
                if IPropertySheet.providedBy(psheet):
                    items = psheet.propertyItems()
                else:
                    items = psheet.items()
                for prop, value in items:
                    properties[prop] = value
        if 'id' in properties:
            # When instantiating sheet(id, **props) is used - two ids is bad
            del properties['id']
        return MutablePropertySheet(self.id,
                                    **properties)
    security.declarePrivate('getPropertiesForUser')

    def setPropertiesForUser(self, user, propertysheet):
        """
        Retrieve all of the IMembraneUserProperties property providers
        and delegate to them.
        """
        prop_providers = self._getPropertyProviders(user)
        for mem_props in prop_providers:
            mem_props.setPropertiesForUser(user, propertysheet)
    security.declarePrivate('setPropertiesForUser')

    def deleteUser(self, user_id):
        """
        XXX: TODO
        """
        pass
    security.declarePrivate('deleteUser')

InitializeClass(MembranePropertyManager)
