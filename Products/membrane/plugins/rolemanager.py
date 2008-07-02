# Copyright 2005 Plone Solutions
# info@plonesolutions.com

from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from Products.membrane.config import TOOLNAME
from Products.membrane.interfaces import IMembraneRoleManagerPlugin
from Products.membrane.interfaces import IMembraneUserRoles

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
    security.declarePrivate('getRolesForPrincipal')
    def getRolesForPrincipal(self, principal, request=None):
        mbtool = getToolByName(self, TOOLNAME)
        uSR = mbtool.unrestrictedSearchResults
        providers = uSR(exact_getUserId=principal.getId(),
                         object_implements=IMembraneUserRoles.__identifier__)
        roles = {}
        for p in providers:
            provider = IMembraneUserRoles(p._unrestrictedGetObject())
            roles.update(dict.fromkeys(provider.getRolesForPrincipal(principal)))
        return tuple(roles.keys())

InitializeClass( MembraneRoleManager )
