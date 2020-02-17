# -*- coding: utf-8 -*-
# Copyright 2005 Plone Solutions
# info@plonesolutions.com

from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.Cache import Cacheable
from Products.membrane.interfaces import group as group_ifaces
from Products.membrane.interfaces import user as user_ifaces
from Products.membrane.utils import findMembraneUserAspect
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin
from Products.PlonePAS.sheet import MutablePropertySheet
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.propertysheets import IPropertySheet  # noqa
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.interface import implementer


manage_addMembranePropertyManagerForm = PageTemplateFile(
    '../www/MembranePropertyManagerForm',
    globals(), __name__='manage_addMembranePropertyManagerForm')


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


@implementer(IPropertiesPlugin, IMutablePropertiesPlugin)
class MembranePropertyManager(BasePlugin, Cacheable):
    """ PAS plugin for managing properties on contentish users and groups
        in Plone.
    """

    meta_type = 'Membrane Property Manager'

    security = ClassSecurityInfo()

    def __init__(self, id, title=None):

        self._id = self.id = id
        self.title = title

    def _getPropertyProviders(self, user):
        isGroup = getattr(user, 'isGroup', lambda: None)()
        if isGroup:
            query = dict(exact_getGroupId=user.getId())
            iface = group_ifaces.IMembraneGroupProperties
        else:
            query = dict(exact_getUserId=user.getId())
            iface = user_ifaces.IMembraneUserProperties

        for pp in findMembraneUserAspect(
                self, iface, **query):
            yield pp

    #
    #   IMutablePropertiesPlugin implementation
    #   IPropertiesPlugin implementation
    #
    @security.private
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

    @security.private
    def setPropertiesForUser(self, user, propertysheet):
        """
        Retrieve all of the IMembraneUserProperties property providers
        and delegate to them.
        """
        prop_providers = self._getPropertyProviders(user)
        for mem_props in prop_providers:
            mem_props.setPropertiesForUser(user, propertysheet)

    @security.private
    def deleteUser(self, user_id):
        """
        XXX: TODO
        """
        pass


InitializeClass(MembranePropertyManager)
