# Copyright 2005 Plone Solutions
# info@plonesolutions.com

from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zope.interface import implements

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.membrane.interfaces.plugins import IMembraneRoleManagerPlugin
from Products.membrane.interfaces import user as user_ifaces
from Products.membrane.utils import findMembraneUserAspect

manage_addMembraneRoleManagerForm = PageTemplateFile(
    '../www/MembraneRoleManagerForm', globals(),
    __name__='manage_addMembraneRoleManager' )


def addMembraneRoleManager(dispatcher, id, title=None, REQUEST=None):
    """ Add a MembraneRoleManager to a Pluggable Auth Service. """
    pmm = MembraneRoleManager(id, title)
    dispatcher._setObject(pmm.getId(), pmm)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'MembraneRoleManager+added.'
                                % dispatcher.absolute_url())


class MembraneRoleManager(BasePlugin, Cacheable):
    """ PAS plugin for managing roles with Membrane.
    """
    meta_type = 'Membrane Role Manager'

    security = ClassSecurityInfo()

    implements(IMembraneRoleManagerPlugin)

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    #   IRolesPlugin implementation
    #
    def getRolesForPrincipal(self, principal, request=None):
        roles = {}
        providers = findMembraneUserAspect(
            self, user_ifaces.IMembraneUserRoles,
            exact_getUserId=principal.getId())
        for provider in providers:
            roles.update(dict.fromkeys(
                provider.getRolesForPrincipal(principal)))
        return tuple(roles.keys())
    security.declarePrivate('getRolesForPrincipal')

InitializeClass(MembraneRoleManager)
