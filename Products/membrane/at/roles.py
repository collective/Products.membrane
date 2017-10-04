# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.membrane.at.interfaces import IUserRoles
from Products.membrane.at.userrelated import UserRelated
from Products.membrane.config import TOOLNAME
from Products.membrane.interfaces import group as group_ifaces
from Products.membrane.interfaces.user import IMembraneUserRoles
from zope.interface import implementer


@implementer(IMembraneUserRoles)
class Roles(UserRelated):
    """
    Adapts from IRolesProvider to IMembraneUserRoles, simply returns
    the roles from the context object.
    """
    security = ClassSecurityInfo()

    #
    #   IRolesPlugin implementation
    #
    @security.private
    def getRolesForPrincipal(self, principal, request=None):
        return IUserRoles(self.context).getRoles()


@implementer(IMembraneUserRoles)
class GroupAwareRoles(UserRelated):
    """
    Adapts from IGroupAwareRolesProvider to
    IMembraneUserRoles. Returns the roles from the roles provider and
    from any groups associated with the principal.
    """
    security = ClassSecurityInfo()

    #
    #   IRolesPlugin implementation
    #
    @security.private
    def getRolesForPrincipal(self, principal, request=None):
        roles = dict.fromkeys(IUserRoles(self.context).getRoles())

        getGroups = getattr(principal, 'getGroups', lambda: tuple())
        group_ids = getGroups()
        if group_ids:
            mbtool = getToolByName(self.context, TOOLNAME)
            uSR = mbtool.unrestrictedSearchResults
            groups = uSR(exact_getGroupId=group_ids,
                         object_implements=(
                             group_ifaces.IGroup.__identifier__))
            for g in groups:
                group = group_ifaces.IGroup(
                    g._unrestrictedGetObject())
                roles.update(dict.fromkeys(group.getRoles()))

        return roles.keys()
